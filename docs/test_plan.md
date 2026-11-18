# Test Plan : OWASP Juice Shop

## 1. Document control

| Field | Value |
|---|---|
| Project | OWASP Juice Shop test automation & manual QA |
| Application under test | OWASP Juice Shop (`bkimminich/juice-shop`) |
| Version tested | v20.2.0-SNAPSHOT |
| Author | |
| Status |  |

## 2. Introduction

This plan covers the testing approach for OWASP Juice Shop, an intentionally
vulnerable e-commerce web application used here as the target for a
combined manual and automated test effort. It defines scope, approach,
environment, schedule, resourcing, entry/exit criteria and risks for one
test cycle, and is intended as a reusable template for future cycles.

## 3. Objectives

- Verify core customer journeys work correctly: registration, login,
  product search/browse, basket management, checkout-adjacent flows,
  feedback and reviews.
- Verify data integrity across layers: UI actions are reflected in the API
  and database, and vice versa.
- Identify functional defects before they reach a shared environment.
- Identify security weaknesses in authentication and input handling
  (SQL injection, broken access control) using both automated probes and
  manual exploratory testing.
- Build a reliable regression test suite that can run automatically in
  a CI pipeline..

## 4. Scope

### 4.1 In scope

| Area | Covered |
|---|---|
| User registration & login | UI, API, DB |
| Product search & browsing | UI, API |
| Basket management |  UI, API, DB, cross-layer |
| Feedback & product reviews | UI, API, DB |
| SQL injection (login, search, product id, feedback) |  |
| Cross-layer consistency (UI ↔ API ↔ DB) |  |

### 4.2 Out of scope (for this cycle)

- Payment/checkout completion and order history
- Administration panel (`/#/administration`) and privilege-escalation
  challenges beyond the login SQLi case already covered
- XSS, IDOR/broken access control, file uploads and business-logic
  challenge categories. These are possible areas for a future test
  cycle. Related markers (`xss`, `access_control`, `business_logic`,
  `file_upload` and `validation`) are already defined in `pytest.ini`.
- Load/performance and accessibility testing
- Mobile browser / responsive layout testing

## 5. Test approach

A layered approach is used, matching the project structure in
`pytest-juice-shop`:

1. **API tests** : fast, direct checks of request/response contracts
   (`tests/api/`).
2. **Database tests** : verify that API/UI actions produce the correct
   rows in the underlying SQLite database (`tests/db/`).
3. **UI tests** : Page-Object-Model Playwright tests for the flows a real
   user would perform (`tests/ui/`).
4. **Integration tests** : deliberately cross layers, e.g. register via
   the UI and confirm the row in the database, or add a basket item via
   the API and confirm it renders in the UI (`tests/integration/`).
5. **Security tests** : targeted SQL-injection probes against login,
   search, product-id and feedback endpoints (`tests/security/`).
6. **Manual/exploratory testing** : the test cases in
   `docs/manual_test_cases.xlsx` are run manually at least once per
   release to catch issues automation does not (visual layout, usability,
   edge cases not yet automated) and to validate new automated tests
   before they are trusted.

Automated tests are the primary regression mechanism; manual testing is
used for exploratory coverage, new-feature sign-off, and triaging any
automated failure before it is logged as a bug.

## 6. Test levels & types

| Type | Technique | Tooling |
|---|---|---|
| Functional | Black-box, equivalence partitioning, boundary values | pytest, Playwright, requests |
| Data integrity | Cross-layer verification | pytest + sqlite3 |
| Security | Known-payload injection, negative testing | pytest + manual Postman/curl |
| Regression | Full suite re-run per change | pytest-xdist (parallel), pytest-rerunfailures (flaky retry) |
| Smoke | Subset tagged `@pytest.mark.smoke` | pytest -m smoke |

## 7. Environment

- Application: Docker container `bkimminich/juice-shop:latest`, started via
  `docker compose up -d` from `docker-compose.yml`, served at
  `http://127.0.0.1:3000`.
- Seed data: `data/juiceshop.sqlite`, mounted into the container so DB
  tests observe the same data the application writes.
- Test runner: Python 3.11+, pytest, Playwright (Chromium by default),
  configuration via `.env` / `config/settings.py`.
- Test data: generated per-test with `utils/helpers.py` (`random_email`,
  `random_password`) to avoid collisions between runs.

## 8. Entry criteria

- Application container is up and passes its health check
  (`GET /rest/admin/application-version` returns 200).
- `pip install -r requirements.txt` and `playwright install` have
  completed without errors.
- `data/juiceshop.sqlite` is present and readable.

## 9. Exit criteria

- 100% of smoke tests (`-m smoke`) pass.
- No new **Critical** or **High** severity defects remain open and
  un-triaged (see `docs/bug_reports.xlsx`).
- All planned manual test cases have a recorded status (Pass/Fail/Blocked),
  not left as "Not Run".
- Known, accepted risks (e.g. intentionally vulnerable challenges that are
  out of scope) are explicitly listed in the release notes, not silently
  skipped.

## 10. Test deliverables

- `docs/manual_test_cases.xlsx`: manual test case catalogue.
- `docs/bug_reports.xlsx`: defect log with reproduction steps and evidence.
- `docs/postman/`: Postman collection + environment for manual/exploratory
  API testing.
- `reports/report.html`: self-contained pytest-html report per automated run.
- This document.
