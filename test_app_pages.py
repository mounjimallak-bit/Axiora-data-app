"""
Smoke test of the Streamlit application: every page of app.py is run headless with Streamlit's
official test harness (streamlit.testing.v1.AppTest) and must finish without an exception.

No browser, no network and no API key are needed; the assistant page only shows its
"no key" message. Writes no file.

Usage:  python test_app_pages.py
Exit code is 1 when a page raises an exception.
"""

import sys

from streamlit.testing.v1 import AppTest

PAGES = ["Accueil", "Population", "Marche de Travail", "Habitat", "Finance", "Enseignement", "pauvrete",
         "Generateur Rapport & statistiques", "assistant axiora data", "Aide & contact"]


def main():
    failures = 0
    for page in PAGES:
        at = AppTest.from_file("app.py", default_timeout=180)
        at.session_state["page"] = page
        at.run()
        status = "PASS" if not at.exception else "FAIL"
        print(f"{status}  {page}: {len(at.exception)} exception(s)")
        for e in at.exception:
            print(f"      {str(e.value)[:300]}")
        failures += len(at.exception)
    print(f"\n{len(PAGES)} pages run, {failures} exception(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
