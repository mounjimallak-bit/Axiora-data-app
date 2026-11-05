"""
Data checks for Axiora.

Reads the hand-typed tables in hcpdata.py and the inline tables in app.py
(parsed as literals, nothing is executed) and reports:

  1. tables whose columns do not have the same number of values
  2. totals that do not match their parts
       - Total column vs Urbain + Rural (and Hommes/Femmes, Masculin/Féminin, Garçons/Filles)
       - TOTAL-x column vs the sum of the other *-x columns
       - aggregate row (Souss-Massa, Total, Ensemble...) vs the sum of the province rows
  3. zeros in rate columns, which usually mean "missing" rather than 0 %
  4. province names that do not reach a shape in the ADM2 shapefile after the
     app's own name mappings, and Souss-Massa communes with the same problem
  5. tables defined both in hcpdata.py and inline in app.py whose values differ

Usage:  python validate_data.py
Exit code is 1 when at least one error is found, so it can run in CI.
"""

import ast
import re
import struct
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ADM2_DBF = ROOT / "mar_admbnda_adm2_hcp_20230925" / "mar_admbnda_adm2_hcp_20230925.dbf"
ADM3_DBF = ROOT / "mar_admbnda_adm3_hcp_20230925" / "mar_admbnda_adm3_hcp_20230925.dbf"
SOUSS_MASSA_PCODE = "MA009"

AGGREGATE_LABELS = {"souss-massa", "souss massa", "total", "ensemble", "region", "région",
                    "t. internationa", "t.national"}
PAIRS = [("Urbain", "Rural"), ("Hommes", "Femmes"), ("Masculin", "Féminin"), ("Garçons", "Filles")]
TOLERANCE = 0.01  # 1 % relative, to allow for rounding in published tables

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ---------------------------------------------------------------- loading
def literal_tables(path):
    """Return {name: dict} for every top-level or nested `x = {...}` literal in a file."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict) \
                and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    return out


def literal_dicts_named(path, name):
    """All literal dicts assigned to `name` (the app defines several mappings with the same name)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name:
            try:
                found.append((node.lineno, ast.literal_eval(node.value)))
            except ValueError:
                pass
    return found


def read_dbf(path):
    """Minimal dBase reader, enough for the attribute table of a shapefile."""
    with open(path, "rb") as f:
        header = f.read(32)
        n_rec, header_len, rec_len = struct.unpack("<IHH", header[4:12])
        fields = []
        while True:
            desc = f.read(32)
            if desc[0] == 0x0D:
                break
            fields.append((desc[:11].split(b"\0")[0].decode(), desc[16]))
        f.seek(header_len)
        rows = []
        for _ in range(n_rec):
            raw = f.read(rec_len)[1:]
            row, pos = {}, 0
            for name, length in fields:
                row[name] = raw[pos:pos + length].decode("utf-8", "replace").strip()
                pos += length
            rows.append(row)
    return rows


def row_table(obj):
    """{row: {col: value}} (the energy tables) -> column table, or None."""
    if obj and all(isinstance(v, dict) and v and all(not isinstance(x, (dict, list)) for x in v.values())
                   for v in obj.values()):
        rows = list(obj)
        cols = list(dict.fromkeys(c for r in rows for c in obj[r]))
        return {"Libellé": rows, **{c: [obj[r].get(c) for r in rows] for c in cols}}
    return None


def iter_tables(obj, path):
    """Yield (path, table) for every column table, including row-oriented ones."""
    if not isinstance(obj, dict):
        return
    if any(isinstance(v, list) for v in obj.values()):
        yield path, obj
        return
    rt = row_table(obj)
    if rt:
        yield path, rt
        return
    for k, v in obj.items():
        if isinstance(v, dict):
            yield from iter_tables(v, f"{path}/{k}")


# ---------------------------------------------------------------- helpers
def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def is_rate(col):
    c = col.lower()
    return bool(re.search(r"(^|[^a-zà-ÿ])taux([^a-zà-ÿ]|$)", c)) or "%" in c or "couverture" in c


def is_rate_table(name, table):
    """Tables of rates cannot be summed. Detected by name, or by values that all look like percentages."""
    n = name.lower()
    if is_rate(n) or "activite_par" in n or "instruction" in n or "diplome" in n:
        return True
    nums = [x for v in table.values() if isinstance(v, list) for x in v if is_num(x)]
    return bool(nums) and all(0 <= x <= 100 for x in nums) and any(isinstance(x, float) and x != int(x) for x in nums)


def is_aggregate(label):
    s = strip_accents(str(label)).lower().strip()
    return s in {strip_accents(a) for a in AGGREGATE_LABELS} or s.startswith("total") or s.startswith("region souss")


def close(a, b):
    return abs(a - b) <= max(1.0, TOLERANCE * max(abs(a), abs(b)))


def strip_accents(s):
    return "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")


def label_column(table):
    for col, values in table.items():
        if isinstance(values, list) and values and all(isinstance(v, str) for v in values):
            return col
    return None


# ---------------------------------------------------------------- checks
def check_lengths(name, table):
    lens = {c: len(v) for c, v in table.items() if isinstance(v, list)}
    if len(set(lens.values())) > 1:
        common = max(set(lens.values()), key=list(lens.values()).count)
        odd = {c: n for c, n in lens.items() if n != common}
        err(f"[length] {name}: most columns have {common} values, but {odd}")
        return False
    return True


def check_column_totals(name, table):
    cols = [c for c, v in table.items() if isinstance(v, list)]
    labels = table.get(label_column(table) or "", None)

    def row_name(i):
        return labels[i] if labels else f"row {i}"

    # Total vs pairs, e.g. "2016 – Total" vs "2016 – Urbain" + "2016 – Rural"
    for c in cols:
        if "total" not in c.lower() or c.upper().startswith("TOTAL-") or is_rate(c):
            continue
        for a, b in PAIRS:
            ca, cb = c.replace("Total", a), c.replace("Total", b)
            if ca in table and cb in table and ca != c:
                for i, (t, x, y) in enumerate(zip(table[c], table[ca], table[cb])):
                    if all(is_num(v) for v in (t, x, y)) and not close(t, x + y):
                        err(f"[total] {name}: {row_name(i)}: {c} = {t} but {a} + {b} = {x + y}")

    # TOTAL-x vs sum of the other *-x columns (tourism table)
    for c in cols:
        if c.upper().startswith("TOTAL-"):
            suffix = c.split("-", 1)[1]
            parts = [p for p in cols if p != c and p.endswith("-" + suffix)]
            for i in range(len(table[c])):
                vals = [table[p][i] for p in parts if i < len(table[p])]
                t = table[c][i]
                if is_num(t) and len(vals) == len(parts) and all(is_num(v) for v in vals):
                    if not close(t, sum(vals)):
                        err(f"[total] {name}: {row_name(i)}: {c} = {t} but the parts sum to {sum(vals)}")


def check_row_totals(name, table):
    lab = label_column(table)
    if not lab or is_rate_table(name, table):
        return
    labels = table[lab]
    norm = [strip_accents(str(x)).lower().strip() for x in labels]
    # Some tables put Morocco-level rows after the regional ones: only the regional block is summed.
    end = next((i for i, x in enumerate(norm) if "maroc" in x), len(labels))
    agg_idx = [i for i in range(end) if is_aggregate(labels[i])]
    if len(agg_idx) != 1:
        return  # no single aggregate row, or several levels: not checked automatically
    a = agg_idx[0]
    parts_idx = [i for i in range(end) if i != a]
    for c, values in table.items():
        if c == lab or not isinstance(values, list) or is_rate(c) or len(values) != len(labels):
            continue
        # None = not published for that row (Tata in the habitat tables): it adds nothing to the total.
        parts = [values[i] for i in parts_idx if values[i] is not None]
        if is_num(values[a]) and parts and all(is_num(p) for p in parts):
            if not close(values[a], sum(parts)):
                err(f"[total] {name}: row '{labels[a]}' column '{c}' = {values[a]} "
                    f"but the other rows sum to {round(sum(parts), 2)}")


def check_zero_rates(name, table):
    lab = label_column(table)
    for c, values in table.items():
        if isinstance(values, list) and is_rate(c):
            zeros = [table[lab][i] if lab else i for i, v in enumerate(values) if v == 0]
            if zeros:
                warn(f"[zero] {name}: '{c}' has 0 for {zeros} (missing value typed as 0?)")


def check_province_names(app_path, tables):
    """Every province name used in a table must reach a polygon through PROVINCE_NAME_MAPPING.
    The maps use an inner join, so a name that does not reach one is dropped from the map silently."""
    shapes = {r["ADM2_FR"] for r in read_dbf(ADM2_DBF) if r["ADM2_PCODE"].startswith(SOUSS_MASSA_PCODE)}
    found = literal_dicts_named(app_path, "PROVINCE_NAME_MAPPING")
    if not found:
        err("[map] PROVINCE_NAME_MAPPING not found in app.py")
        return
    lineno, mapping = found[0]
    for src, dst in mapping.items():
        if dst not in shapes:
            err(f"[map] app.py line {lineno}: '{src}' is mapped to '{dst}', which is not a province "
                f"in the shapefile {sorted(shapes)}")
    names = set()
    for _, table in tables:
        for col in ("Province", "Provinces"):
            if isinstance(table.get(col), list):
                names.update(x for x in table[col] if isinstance(x, str))
    for n in sorted(names):
        if is_aggregate(n) or strip_accents(n).lower() in {"maroc", "region souss-massa", "region"}:
            continue
        if mapping.get(n, n) not in shapes:
            err(f"[map] province name '{n}' does not reach any polygon of the shapefile "
                f"(add it to PROVINCE_NAME_MAPPING in app.py)")


def check_commune_names(app_path):
    tables = literal_tables(app_path)
    pauvrete = tables.get("pauvrete_data")
    mapping_list = literal_dicts_named(app_path, "commune_name_mapping")
    if not pauvrete:
        return
    mapping = mapping_list[0][1] if mapping_list else {}

    def clean(s):  # same as nettoyer_nom in app.py
        return s.lower().replace("(m)", "").replace("(ac)", "").replace("-", " ").replace("'", " ").strip()

    shapes = {clean(r["ADM3_FR"]) for r in read_dbf(ADM3_DBF) if r["ADM2_PCODE"].startswith(SOUSS_MASSA_PCODE)}
    keys = []
    for prov, data in pauvrete.items():
        for c in data["Commune"]:
            if "Province de" in c or "Préfecture d" in c or "(AC)" in c:
                continue  # aggregates and centres, excluded from the map in app.py
            k = clean(c)
            keys.append((prov, c, mapping.get(k, k)))
    missing = [(p, c) for p, c, k in keys if k not in shapes]
    for p, c in missing:
        warn(f"[map] commune '{c}' ({p}) does not match any commune in the shapefile and is not drawn")
    from collections import Counter
    dup = [k for k, n in Counter(k for _, _, k in keys).items() if n > 1 and k in shapes]
    for k in dup:
        names = [c for _, c, kk in keys if kk == k]
        err(f"[map] several rows are drawn on the same commune polygon '{k}': {names}")
    covered = {k for _, _, k in keys}
    not_covered = sorted(shapes - covered)
    if not_covered:
        warn(f"[map] {len(not_covered)} Souss-Massa communes in the shapefile have no data row: {not_covered}")


def check_duplicates(hcp, app_tables):
    """Compare tables that exist in both hcpdata.py and app.py."""
    pairs = [("pauvrete", "pauvrete_data")]
    for hk, ak in pairs:
        if hk in hcp and ak in app_tables:
            a, b = hcp[hk], app_tables[ak]
            for prov in sorted(set(a) | set(b)):
                if prov not in a or prov not in b:
                    warn(f"[copy] '{prov}' is in only one of hcpdata.py['{hk}'] and app.py {ak}")
                    continue
                for col in set(a[prov]) & set(b[prov]):
                    if a[prov][col] != b[prov][col]:
                        err(f"[copy] '{prov}' / '{col}' differs between hcpdata.py['{hk}'] and app.py {ak}")


# ---------------------------------------------------------------- main
# Tables whose "Total" column is the sum of named columns (beyond the Urbain/Rural pairs).
COLUMN_SUMS = {
    "nombre_consommateurs_par_type_tension": ("Total", ["Basse tension", "Moyenne tension", "Haute tension"]),
    "eleves_primaire_public_par_niveau": ("Total", ["1ère", "2ème", "3ème", "4ème", "5ème", "6ème"]),
    "Élèves par classe": ("Total", ["1ère", "2ème", "3ème", "4ème", "5ème", "6ème"]),
    "lits_hopitaux_publics_2017": ("Total", ["Hôpitaux généraux", "Hôpitaux spécialisés"]),
    "population_chomage_age_milieu": ("Total", ["15-24", "25-34", "35-44", "45+"]),
    "population_active_occupee_secteurs": ("Total", ["Forêt et pêche / Agriculture", "Industrie et commerce",
                                                      "B.T.P", "Services", "Autres"]),
    "population_active_occupee_sexe": ("Total", ["Masculin", "Féminin"]),
}


def check_named_sums(name, table):
    for key, (tot, parts) in COLUMN_SUMS.items():
        if not name.endswith(key) and f"/{key}/" not in name:
            continue
        if tot not in table or not all(p in table for p in parts):
            continue
        labels = table.get(label_column(table) or "", None)
        for i, t in enumerate(table[tot]):
            vals = [table[p][i] for p in parts]
            if is_num(t) and all(is_num(v) for v in vals) and not close(t, sum(vals)):
                row = labels[i] if labels else i
                err(f"[total] {name}: {row}: {tot} = {t} but {' + '.join(parts)} = {sum(vals)}")


def main():
    hcp = literal_tables(ROOT / "hcpdata.py")["hcp_data"]
    app = literal_tables(ROOT / "app.py")

    tables = list(iter_tables(hcp, "hcpdata"))
    for name, obj in app.items():
        tables += list(iter_tables(obj, f"app.py:{name}"))

    for name, table in tables:
        ok = check_lengths(name, table)
        if ok:
            check_column_totals(name, table)
            check_row_totals(name, table)
            check_named_sums(name, table)
        check_zero_rates(name, table)

    check_province_names(ROOT / "app.py", tables)
    check_commune_names(ROOT / "app.py")
    check_duplicates(hcp, app)

    print(f"{len(tables)} tables checked\n")
    for title, items in (("ERRORS", errors), ("WARNINGS", warnings)):
        print(f"{title} ({len(items)})")
        for m in items:
            print("  " + m)
        print()
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
