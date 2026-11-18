# Testing Approach

This document explains how testing is organised for this project, and how
the pieces in `docs/` relate to the automated suite in `tests/`.

## Testing Principles

Automation and manual testing are treated as complementary, not
competing:

- **Automation** gives fast, repeatable regression coverage across four
  layers (UI, API, database, cross-layer integration) plus a set of
  targeted security probes, and is what runs on every change.
- **Manual testing** is used to design new coverage before it is
  automated, to explore areas automation doesn't reach yet (visual
  details, ambiguous edge cases, exploratory security testing), and to
  independently verify automated findings.

## Test pyramid for this project

```
          ┌───────────────────────┐
          │   Manual / exploratory| 
          ├───────────────────────┤
          │     UI (Playwright)   |
          ├───────────────────────┤
          │  Integration (cross-  |
          │   layer: UI+API+DB)   |
          ├───────────────────────┤
          │   Security (SQLi etc.)|
          ├───────────────────────┤
          │   Database (SQLite)   |
          ├───────────────────────┤
          │     API (requests)    |   
          └───────────────────────┘
```


## How Defects Are Managed

1. **Found**:  A defect is identified either by an automated test failure (pytest/CI) or during manual and exploratory testing using `docs/manual_test_cases.xlsx`.
2. **Reproduced**: The defect is checked to confirm that it can be repeated. Each entry in `docs/bug_reports.xlsx` includes clear steps to reproduce the issue, such as API requests, payloads or UI actions.
3. **Reviewed and Classified**: Each defect is reviewed and assigned a severity and priority. Since the application is intentionally vulnerable, security findings are also checked to determine whether they are known OWASP Juice Shop challenges or unexpected issues. Both types are recorded and clearly identified.
4. **Recorded**: All confirmed defects are documented in `docs/bug_reports.xlsx`. Where applicable, the related automated test is also included to show how the issue was identified (for example, `test_sec07_login_sql_injection_bypass_is_blocked`).
5. **Retested**: After a defect is fixed, it is tested again to make sure the issue is resolved. An existing automated test is reused where possible. If the defect was originally found through manual testing, a new automated regression test is added where appropriate.

## What's covered where

| Document / folder | Purpose |
|---|---|
| `tests/` | The automated pytest + Playwright suite (source of truth for regression) |
| `docs/test_plan.md` | Scope, approach, environment, entry/exit criteria for a test cycle |
| `docs/manual_test_cases.xlsx` | Manual test case catalogue, cross-referenced to the automated test that also covers each case where one exists |
| `docs/bug_reports.xlsx` | Defects found during this project, with reproduction steps and evidence |
| `docs/postman/` | A Postman collection + environment for manual/exploratory API testing and for demonstrating findings (e.g. the login SQL-injection bypass) outside of pytest |
| `reports/report.html` | Generated HTML report from the most recent automated run |

## Security testing notes

OWASP Juice Shop is intentionally designed with security weaknesses. This means that finding vulnerabilities is part of the testing process. The following approach is used to make sure security findings are properly checked and recorded:

- **Security Tests** – Tests in `tests/security/` check whether the application behaves securely. For example, a SQL injection attempt should not allow a user to log in. If a test fails, it highlights a potential security issue that needs further investigation.
- **Recording Security Findings** – Every failed security test is investigated and documented in `docs/bug_reports.xlsx`. Each report includes clear evidence, such as the exact payload used and the response received (including JWT details where relevant), rather than simply stating that a test failed.

    For example, **BUG-001** documents a SQL injection issue in the login form. Testing confirmed that it allowed access as `admin@juice-sh.op` without a valid password.
- **Test Script Issues** – Not every failed test means there is a problem with the application. Sometimes the issue is in the test script itself, such as an incorrect or overly broad CSS locator. These findings are also recorded and clearly labelled so they can be distinguished from actual application defects.

## Running everything

```bash
# full automated suite
pytest

# one layer at a time
pytest -m ui
pytest -m api
pytest -m db
pytest -m integration
pytest -m sqli

# smoke subset
pytest -m smoke

# parallel + flaky-retry
pytest -n 4 --reruns 2
```

See the root `README.md` for environment setup (Docker, virtualenv,
`playwright install`) and `docs/test_plan.md` for the fuller process this
testing approach sits inside.
