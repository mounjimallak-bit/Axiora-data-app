"""Numerical checks of the mathematical notes of the Axiora case study.

Read-only (writes no file). Run from the repository root:

    python math_checks_axiora.py

Tables are read from hcpdata.py as literals, exactly as the app, validate_data.py and
analyse_pauvrete.py read them; the commune map join reuses validate_data.py's rule.
Requires only packages of requirements.txt (numpy, pandas, geopandas).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent


def spearman(a, b):
    return pd.Series(a).rank().corr(pd.Series(b).rank())


def skewness(x):
    z = x - x.mean()
    return (z ** 3).mean() / (z ** 2).mean() ** 1.5
sys.path.insert(0, str(ROOT))
import validate_data as vd  # noqa: E402  (functions only; its checks run under __main__)

hcp = vd.literal_tables(ROOT / "hcpdata.py")["hcp_data"]
POP = pd.DataFrame(hcp["population"]["population_legale"]).set_index("Provinces")
ORDER = ["Agadir-Ida -Ou-Tanane", "Inezgane-Ait Melloul", "Chtouka- Ait Baha", "Taroudannt", "Tiznit", "Tata"]
POP_NAME = dict(zip(ORDER, ["Agadir Ida Outanane", "Inezgane-Aït Melloul", "Chtouka-Aït Baha", "Taroudant", "Tiznit", "Tata"]))

print("1. A weighted mean identifies its weights: urban share implied by the published rates")
print("   E = w U + (1 - w) R  =>  w = (E - R) / (U - R); interval from rounding of the published rates")
for year, half in ((2004, 0.05), (2014, 0.005)):
    print(f"   {year} (rates rounded to {'one' if half == 0.05 else 'two'} decimal{'s' if half < 0.05 else ''})")
    for p in ORDER:
        t = pd.DataFrame(hcp["pauvrete"][p])
        col = f"Taux de pauvreté {year}"
        U = t.loc[t["Commune"].str.endswith("Urbain"), col].item()
        R = t.loc[t["Commune"].str.endswith("Rural"), col].item()
        E = t.loc[t["Commune"].str.endswith("Ensemble"), col].item()
        w = (E - R) / (U - R)
        corners = [((E + a) - (R + c)) / ((U + b) - (R + c)) for a in (-half, half) for b in (-half, half) for c in (-half, half)]
        census = POP.loc[POP_NAME[p], f"RGPH {year} – Urbain"] / POP.loc[POP_NAME[p], f"RGPH {year} – Total"]
        print(f"     {p:24s} implied w = {w:.3f}  [{min(corners):.3f}, {max(corners):.3f}]   census urban share = {census:.3f}")

rows = pd.concat([pd.DataFrame(d).assign(Territoire=p) for p, d in hcp["pauvrete"].items()], ignore_index=True)
units = rows[~rows["Commune"].str.contains("Province de|Préfecture d", regex=True)]
units = units.dropna(subset=["Taux de pauvreté 2004", "Taux de pauvreté 2014"]).reset_index(drop=True)
p04, p14 = units["Taux de pauvreté 2004"].to_numpy(), units["Taux de pauvreté 2014"].to_numpy()
d = p14 - p04

print(f"\n2. Location, spread and shape of the {len(units)} unit rates")
for name, x in (("2004", p04), ("2014", p14), ("change", d)):
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    print(f"   {name:6s}: mean {x.mean():6.2f} | median {med:6.2f} | IQR {q3 - q1:5.2f} | sd {x.std(ddof=1):5.2f} | "
          f"skewness {skewness(x):+.2f} | MAD {np.median(np.abs(x - np.median(x))):.2f}")

print("\n3. Change against initial level (regression towards the mean)")
slope, icpt = np.polyfit(p04, d, 1)
r = np.corrcoef(p04, d)[0, 1]
print(f"   change 2014-2004 on 2004 rate: slope {slope:.3f}, intercept {icpt:.2f}, Pearson r = {r:.2f}, "
      f"Spearman = {spearman(p04, d):.2f}")
rel = d / p04
print(f"   relative change on 2004 rate: Spearman = {spearman(p04, rel):.2f}  "
      f"(median relative change {np.median(rel):.1%})")
print(f"   variance 2004 = {p04.var(ddof=1):.1f}, variance 2014 = {p14.var(ddof=1):.1f}, cov = {np.cov(p04, p14)[0, 1]:.1f}, "
      f"corr(2004, 2014) = {np.corrcoef(p04, p14)[0, 1]:.2f}")

print("\n4. How much of the variation lies between territories (one-way decomposition)")
for name, col in (("2004", "Taux de pauvreté 2004"), ("2014", "Taux de pauvreté 2014")):
    g = units.groupby("Territoire")[col]
    ssb = (g.size() * (g.mean() - units[col].mean()) ** 2).sum()
    sst = ((units[col] - units[col].mean()) ** 2).sum()
    print(f"   {name}: share of the total sum of squares between territories = {ssb / sst:.2f}")

print("\n5. Spatial autocorrelation: Moran's I on the commune map (queen contiguity)")
import geopandas as gpd
app = ROOT / "app.py"
mapping = vd.literal_dicts_named(app, "commune_name_mapping")[-1][1]
provinces = vd.literal_dicts_named(app, "province_vers_adm2")[-1][1]
clean = lambda s: s.lower().replace("(m)", "").replace("(ac)", "").replace("-", " ").replace("'", " ").strip()  # noqa: E731
shp = gpd.read_file(vd.ADM3_DBF.with_suffix(".shp"))
shp = shp[shp["ADM1_PCODE"] == vd.SOUSS_MASSA_PCODE].copy()
shp["key"] = list(zip(shp["ADM2_FR"], shp["ADM3_FR"].map(clean)))
c = units[~units["Commune"].str.contains(r"\(AC\)", regex=True)].copy()
c["key"] = [(provinces[p], mapping.get(clean(n), clean(n))) for p, n in zip(c["Territoire"], c["Commune"])]
m = shp.merge(c, on="key", how="inner").reset_index(drop=True)
print(f"   communes joined to a polygon: {len(m)} (urban centre units have no polygon of their own)")
geom = m.geometry.buffer(0)
n = len(m)
W = np.zeros((n, n))
sidx = geom.sindex
for i, g in enumerate(geom):
    for j in sidx.query(g, predicate="intersects"):
        if j != i:
            W[i, j] = 1.0
deg = W.sum(axis=1)
print(f"   neighbours per commune: median {np.median(deg):.0f}, min {deg.min():.0f}, max {deg.max():.0f}; "
      f"isolated: {int((deg == 0).sum())}")
rng = np.random.default_rng(0)
def moran(x):
    z = x - x.mean()
    return n / W.sum() * (z @ W @ z) / (z @ z)
for name, x in (("2004 rate", m["Taux de pauvreté 2004"].to_numpy()), ("2014 rate", m["Taux de pauvreté 2014"].to_numpy()),
                ("change 2004-2014", (m["Taux de pauvreté 2014"] - m["Taux de pauvreté 2004"]).to_numpy())):
    I = moran(x)
    perm = np.array([moran(rng.permutation(x)) for _ in range(9999)])
    p = (1 + (np.abs(perm - perm.mean()) >= abs(I - perm.mean())).sum()) / (1 + len(perm))
    print(f"   {name:16s}: I = {I:.3f} | E[I] under no association = {-1 / (n - 1):.4f} | "
          f"permutation mean {perm.mean():.4f}, sd {perm.std():.3f} | two-sided p = {p:.4f}")
