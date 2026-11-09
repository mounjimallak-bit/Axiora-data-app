"""
Tests of validate_data.py: each test copies the data files to a temporary folder, introduces one
error on purpose, runs the validator there and checks that the error is reported. The last test
checks that the unmodified data pass.

Usage:  python test_validate_data.py
Exit code is 1 when a test fails.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = ["validate_data.py", "hcpdata.py", "app.py"]
FOLDERS = ["mar_admbnda_adm2_hcp_20230925", "mar_admbnda_adm3_hcp_20230925"]


def run_validator(edits):
    """edits: list of (file, old text, new text). Returns the number of errors reported."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for f in FILES:
            shutil.copy(ROOT / f, tmp / f)
        for d in FOLDERS:
            shutil.copytree(ROOT / d, tmp / d)
        for f, old, new in edits:
            text = (tmp / f).read_text(encoding="utf-8")
            if old not in text:
                raise AssertionError(f"test setup: text not found in {f}: {old[:60]}")
            (tmp / f).write_text(text.replace(old, new), encoding="utf-8")
        out = subprocess.run([sys.executable, "validate_data.py"], cwd=tmp,
                             capture_output=True, text=True).stdout
    return int(re.search(r"ERRORS \((\d+)\)", out).group(1))


BOTH = ("hcpdata.py", "app.py")  # an error typed in both copies: only the totals can catch it

TESTS = [
    # (description, edits, errors expected?)
    ("no change: the data pass", [], False),
    ("count total off by 1 (teaching staff, Agadir 2017: 1791 -> 1792), in both copies",
     [(f, "[1791, 1647, 1922, 5258, 1222, 819, 12659]", "[1792, 1647, 1922, 5258, 1222, 819, 12659]")
      for f in BOTH], True),
    ("regional population 2014 +20 000 (0.75 %), in both copies",
     [(f, "2676847", "2696847") for f in BOTH], True),
    ("Total Communes off by 1 (Agadir 2017: 13 -> 14), in both copies",
     [(f, '"Total Communes": [13, 6, 22, 89, 25, 20]', '"Total Communes": [14, 6, 22, 89, 25, 20]')
      for f in BOTH], True),
    ("app.py copy differs from hcpdata.py (unemployment rate, region: 13.9 -> 14.7)",
     [("app.py", '"Taux_Chômage_Urbain": [16.7, 11.8, 13.8, 13.9]',
       '"Taux_Chômage_Urbain": [16.7, 11.8, 13.8, 14.7]')], True),
    ("2018 enrolment table of app.py filled with the 2017 figures",
     [("app.py", "[6233, 6236, 4961, 9248, 1923, 1288, 29889],\n                         \"Filles\": "
                 "[6187, 6016, 4666, 8826, 1905, 1152, 28752],\n                         \"Total\": "
                 "[12420, 12252, 9627, 18074, 3826, 2440, 58639]",
       "[6237, 6043, 4605, 9112, 1886, 1190, 29073],\n                         \"Filles\": "
       "[5950, 5750, 4383, 8784, 1758, 1178, 27803],\n                         \"Total\": "
       "[12187, 11793, 8988, 17896, 3644, 2368, 56876]")], True),
    ("housing table 'en étude' of app.py filled with the 'achevées' figures (cost column)",
     [("app.py", '"Cout en Millions de DH": [5815, 110, 77, 40, 55, None, 6097]',
       '"Cout en Millions de DH": [588, 285, 2, 36, 60, None, 971]')], True),
]


def main():
    failed = 0
    for description, edits, expect_errors in TESTS:
        n = run_validator(edits)
        ok = (n > 0) == expect_errors
        failed += not ok
        verdict = "detected" if n else "no error"
        print(f"{'PASS' if ok else 'FAIL'}  {description}: {verdict} ({n})")
    print(f"\n{len(TESTS) - failed}/{len(TESTS)} tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
