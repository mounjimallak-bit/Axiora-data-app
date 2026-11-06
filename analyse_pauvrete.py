"""
Poverty analysis for the Axiora case study (Souss-Massa, 2004, 2007, 2014).

Reproduces every number in the "Results" and "Population and sectors" sections of
the case study from the tables in hcpdata.py. Nothing is typed by hand here: the
tables are read from hcpdata.py exactly as the app and validate_data.py read them.

Usage:  python analyse_pauvrete.py           (prints the results)
        python analyse_pauvrete.py --figures (also writes the two box plots to figures/)

Requires pandas, numpy, scipy (and matplotlib for --figures).
"""

import ast
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy import stats

ROOT = Path(__file__).resolve().parent
YEARS = (2004, 2007, 2014)
COLS = [f"Taux de pauvreté {y}" for y in YEARS]
N_BOOT, SEED = 10_000, 42


def load_hcp_data():
    """hcp_data from hcpdata.py, parsed as a literal (the file is never executed)."""
    tree = ast.parse((ROOT / "hcpdata.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "hcp_data" for t in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError("hcp_data not found in hcpdata.py")


def poverty_units(hcp):
    """One row per commune or urban centre unit; province and prefecture subtotals removed."""
    df = pd.concat([pd.DataFrame(d).assign(Territoire=p) for p, d in hcp["pauvrete"].items()],
                   ignore_index=True)
    subtotal = df["Commune"].str.contains("Province de|Préfecture d", regex=True)
    return df[~subtotal].reset_index(drop=True)


def r1(v):
    """Round half up to one decimal (11.65 -> 11.7), the convention used on the page."""
    return f"{np.floor(v * 10 + 0.5) / 10:.1f}"


def pct(x):
    return f"{r1(x)}%"


def main(figures=False):
    hcp = load_hcp_data()
    units = poverty_units(hcp)
    sample = units.dropna(subset=COLS).reset_index(drop=True)
    excluded = units[units[COLS].isna().any(axis=1)]
    x, y, z = (sample[c].to_numpy() for c in COLS)
    d = z - x

    print("=== Sample ===")
    print(f"Geographic units after removing subtotals: {len(units)}")
    is_ac = sample["Commune"].str.contains("(AC)", regex=False)
    print(f"Complete-case sample: {len(sample)} ({(~is_ac).sum()} communes, {is_ac.sum()} urban centre units)")
    for _, r in excluded.iterrows():
        missing = [str(yr) for yr, c in zip(YEARS, COLS) if pd.isna(r[c])]
        print(f"  excluded: {r.Commune} ({r.Territoire}), no rate in {' and '.join(missing)}")

    print("\n=== Distribution across the region ===")
    for yr, v in zip(YEARS, (x, y, z)):
        q1, med, q3 = np.percentile(v, [25, 50, 75])
        print(f"{yr}: Q1 {pct(q1)}  median {pct(med)}  Q3 {pct(q3)}  mean {pct(v.mean())}  IQR {r1(q3 - q1)} pts")
    m = [np.median(v) for v in (x, y, z)]
    print(f"Median 2004 -> 2014: {m[0] - m[2]:.1f} points ({(m[0] - m[2]) / m[0]:.1%} of the 2004 median)")
    print(f"Median change 2004 -> 2007: {m[0] - m[1]:.1f} points; 2007 -> 2014: {m[1] - m[2]:.1f} points")

    print("\n=== Change by geographic unit (2014 minus 2004) ===")
    n_dec = int((d < 0).sum())
    print(f"Declines: {n_dec} of {len(d)} ({n_dec / len(d):.1%}); zero changes: {int((d == 0).sum())}")
    print(f"Largest increase {d.max():.1f} points; largest decline {d.min():.1f} points")
    rng = np.random.default_rng(SEED)
    boot = np.array([np.median(rng.choice(d, len(d))) for _ in range(N_BOOT)])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print(f"Median change {np.median(d):.1f} points, 95% percentile bootstrap CI "
          f"[{lo:.1f}, {hi:.1f}] ({N_BOOT} resamples, seed {SEED})")
    sign = stats.binomtest(n_dec, len(d), 0.5, alternative="two-sided")
    print(f"Exact sign test: {n_dec}/{len(d)}, two-sided p = {sign.pvalue:.1e}")
    w = stats.wilcoxon(x, z, alternative="two-sided")
    print(f"Wilcoxon signed-rank (SciPy {scipy.__version__}): W = {w.statistic:.0f}, "
          f"p = {w.pvalue:.1e}; skewness of changes {stats.skew(d):.1f}")

    print("\n=== By territory ===")
    sample["Changement"] = d
    order = ["Agadir-Ida -Ou-Tanane", "Inezgane-Ait Melloul", "Chtouka- Ait Baha",
             "Taroudannt", "Tiznit", "Tata"]
    for t in order:
        g = sample[sample.Territoire == t]
        print(f"{t:24s} units {len(g):3d}  median 2004 {r1(g[COLS[0]].median())}%  "
              f"median 2014 {r1(g[COLS[2]].median())}%  median change {r1(g.Changement.median())}  "
              f"declines {(g.Changement < 0).sum()} of {len(g)}")

    print("\n=== Population and sectors ===")
    pl = pd.DataFrame(hcp["population"]["population_legale"]).set_index("Provinces")
    growth = pl["RGPH 2014 – Total"] / pl["RGPH 2004 – Total"] - 1
    print(f"Region: {pl.loc['Souss-Massa', 'RGPH 2004 – Total']:,} -> "
          f"{pl.loc['Souss-Massa', 'RGPH 2014 – Total']:,} ({growth['Souss-Massa']:+.1%})")
    for p, g in growth.drop("Souss-Massa").items():
        print(f"  {p}: {g:+.1%}")
    bank = pd.DataFrame(hcp["finance"]["depots_credits_banques"]).set_index("Province")
    dep, cred = bank["Montant des dépôts (en milliers)"], bank["Montant des crédits (en milliers)"]
    print(f"Credit / deposits: {cred.sum() / 1e6:.2f} / {dep.sum() / 1e6:.2f} billion DH "
          f"= {cred.sum() / dep.sum():.1%}; highest: {(cred / dep).idxmax()} {(cred / dep).max():.1%}")

    if figures:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        out = ROOT / "figures"
        out.mkdir(exist_ok=True)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.boxplot([x, y, z], tick_labels=[str(v) for v in YEARS], showfliers=True)
        ax.set_ylabel("Poverty rate (%)")
        ax.set_title(f"Poverty rates across {len(sample)} geographic units")
        fig.tight_layout(); fig.savefig(out / "pauvrete_distribution.png", dpi=150)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.boxplot([sample.loc[sample.Territoire == t, "Changement"] for t in order],
                   tick_labels=["Agadir", "Inezgane", "Chtouka", "Taroudant", "Tiznit", "Tata"])
        ax.axhline(0, ls="--", color="grey")
        ax.set_ylabel("Change 2014 minus 2004 (points)")
        fig.tight_layout(); fig.savefig(out / "pauvrete_changement_territoire.png", dpi=150)
        print(f"\nFigures written to {out}/")


if __name__ == "__main__":
    main(figures="--figures" in sys.argv)
