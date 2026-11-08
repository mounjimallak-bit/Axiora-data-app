

import ast
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
YEARS = (2004, 2007, 2014)
COLS = [f"Taux de pauvreté {y}" for y in YEARS]
ORDER = ["Agadir-Ida -Ou-Tanane", "Inezgane-Ait Melloul", "Chtouka- Ait Baha",
         "Taroudannt", "Tiznit", "Tata"]
SHORT = ["Agadir", "Inezgane", "Chtouka", "Taroudant", "Tiznit", "Tata"]


def load_hcp_data():
    """hcp_data from hcpdata.py, parsed as a literal (the file is never executed)."""
    tree = ast.parse((ROOT / "hcpdata.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "hcp_data" for t in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError("hcp_data not found in hcpdata.py")


def poverty_rows(hcp):
    return pd.concat([pd.DataFrame(d).assign(Territoire=p) for p, d in hcp["pauvrete"].items()],
                     ignore_index=True)


def poverty_units(rows):
    """One row per commune or urban centre unit; province and prefecture subtotals removed."""
    subtotal = rows["Commune"].str.contains("Province de|Préfecture d", regex=True)
    return rows[~subtotal].reset_index(drop=True)


def territory_rates(rows):
    """The population-weighted rate of each territory: its published "Ensemble" row."""
    ens = rows[rows["Commune"].str.contains(r"^(?:Province de|Préfecture d).* Ensemble$", regex=True)]
    assert sorted(ens["Territoire"]) == sorted(ORDER) and len(ens) == len(ORDER), ens["Commune"].tolist()
    return ens.set_index("Territoire").loc[ORDER, COLS]


def r1(v):
    """Round half up to one decimal (11.65 -> 11.7), the convention used on the page."""
    return f"{np.floor(v * 10 + 0.5) / 10:.1f}"


def pct(x):
    return f"{r1(x)}%"


def main(figures=False):
    hcp = load_hcp_data()
    rows = poverty_rows(hcp)
    units = poverty_units(rows)
    sample = units.dropna(subset=COLS).reset_index(drop=True)
    excluded = units[units[COLS].isna().any(axis=1)]
    x, y, z = (sample[c].to_numpy() for c in COLS)
    d = z - x

    print("=== Geographic units ===")
    print(f"Geographic units after removing subtotals: {len(units)}")
    is_ac = sample["Commune"].str.contains("(AC)", regex=False)
    print(f"Units with a rate in all three years: {len(sample)} ({(~is_ac).sum()} communes, "
          f"{is_ac.sum()} urban centre units)")
    for _, r in excluded.iterrows():
        missing = [str(yr) for yr, c in zip(YEARS, COLS) if pd.isna(r[c])]
        print(f"  excluded: {r.Commune} ({r.Territoire}), no rate in {' and '.join(missing)}")

    print("\n=== Distribution across the region (each unit counts once) ===")
    for yr, v in zip(YEARS, (x, y, z)):
        q1, med, q3 = np.percentile(v, [25, 50, 75])
        print(f"{yr}: Q1 {pct(q1)}  median {pct(med)}  Q3 {pct(q3)}  mean {pct(v.mean())}  IQR {r1(q3 - q1)} pts")
    m = [np.median(v) for v in (x, y, z)]
    print(f"Median 2004 -> 2014: {m[0] - m[2]:.1f} points ({(m[0] - m[2]) / m[0]:.1%} of the 2004 median)")
    print(f"Median change 2004 -> 2007: {m[0] - m[1]:.1f} points; 2007 -> 2014: {m[1] - m[2]:.1f} points")

    print("\n=== Change by geographic unit (2014 minus 2004) ===")
    n_dec = int((d < 0).sum())
    print(f"Declines: {n_dec} of {len(d)} ({n_dec / len(d):.1%}); increases: {int((d > 0).sum())}; "
          f"zero changes: {int((d == 0).sum())}")
    print(f"Largest increase {d.max():.1f} points; largest decline {d.min():.1f} points")
    print(f"Median change {np.median(d):.1f} points; quartiles of the change "
          f"{np.percentile(d, 25):.1f} and {np.percentile(d, 75):.1f} points")

    print("\n=== By territory: units counted once ===")
    sample["Changement"] = d
    for t in ORDER:
        g = sample[sample.Territoire == t]
        print(f"{t:24s} units {len(g):3d}  median 2004 {r1(g[COLS[0]].median())}%  "
              f"median 2014 {r1(g[COLS[2]].median())}%  median change {r1(g.Changement.median())}  "
              f"declines {(g.Changement < 0).sum()} of {len(g)}")

    print("\n=== By territory: population-weighted rate published by the HCP (\"Ensemble\" row) ===")
    w = territory_rates(rows)
    w["Change (points)"] = w[COLS[2]] - w[COLS[0]]
    w["Change (% of 2004)"] = 100 * w["Change (points)"] / w[COLS[0]]
    for t, r in w.iterrows():
        print(f"{t:24s} 2004 {r[COLS[0]]:5.1f}%  2007 {r[COLS[1]]:5.1f}%  2014 {r[COLS[2]]:5.2f}%  "
              f"change {r['Change (points)']:+6.2f} points  ({r['Change (% of 2004)']:+.1f}%)")
    print("Smallest decline in points:", w["Change (points)"].idxmax(),
          f"({w['Change (points)'].max():+.2f}); smallest relative decline:",
          w["Change (% of 2004)"].idxmax(), f"({w['Change (% of 2004)'].max():+.1f}%)")
    print("Highest 2014 rate:", w[COLS[2]].idxmax(), f"({w[COLS[2]].max():.2f}%); lowest:",
          w[COLS[2]].idxmin(), f"({w[COLS[2]].min():.2f}%)")
    rank_units = sample.groupby("Territoire")["Changement"].median().loc[ORDER].rank(ascending=False)
    rank_w = w["Change (points)"].rank(ascending=False)
    print("Rank of the decline, 1 = smallest (units median / weighted points):",
          ", ".join(f"{s} {int(a)}/{int(b)}" for s, a, b in zip(SHORT, rank_units, rank_w)))

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
        ax.boxplot([sample.loc[sample.Territoire == t, "Changement"] for t in ORDER], tick_labels=SHORT)
        ax.plot(range(1, len(ORDER) + 1), w["Change (points)"], "D", color="#b5432f",
                label="Population-weighted change of the territory (HCP)")
        ax.axhline(0, ls="--", color="grey")
        ax.set_ylabel("Change 2014 minus 2004 (points)")
        ax.legend(loc="lower left", fontsize=8)
        fig.tight_layout(); fig.savefig(out / "pauvrete_changement_territoire.png", dpi=150)
        print(f"\nFigures written to {out}/")


if __name__ == "__main__":
    main(figures="--figures" in sys.argv)
