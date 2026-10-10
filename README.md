# Pytest + Playwright Test Automation Framework for OWASP Juice Shop

A complete testing framework for [OWASP Juice Shop](https://owasp-juice.shop)
built with **Python, pytest** and **Playwright**, covering **UI, API, database,
security, and cross-layer integration testing** **about 70 test cases** in total.

## Features

- **UI tests** using the Page Object Model (POM) with Playwright
- **API tests** through a reusable `requests`-based client
- **Database tests** that verify application state directly in the Juice Shop SQLite database (read-only connection)
- **Integration tests** that cross layers, e.g. register via the UI and confirm the row in the database, or add a basket item via the API and see it in the UI
- **Security tests** covering SQL injection against search, product, feedback and login endpoints
- **Reusable fixtures** for browsers, API clients, database access, randomly generated test users and authenticated sessions
- **Parallel execution** with `pytest-xdist` and **flaky-test retries** with `pytest-rerunfailures`
- **Self-contained HTML reports**, plus screenshots and Playwright traces retained on failure
- **Dockerised target application** with a health check, started with one command

## Project Structure

```
pytest-juice-shop/
├── api/
│   └── api_client.py          # Reusable API client (users, products, baskets, feedback, ...)
├── config/
│   └── settings.py            # Central configuration, overridable via .env
├── data/
│   └── juiceshop.sqlite       # Juice Shop database, mounted into the container
├── db/
│   └── database.py            # SQLite helper with read-only queries
├── pages/                     # Page Object Model
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── basket_page.py
│   ├── product_page.py
│   └── contact_page.py
├── tests/
│   ├── ui/                    # UI tests
│   ├── api/                   # API tests
│   ├── db/                    # Database verification tests
│   ├── integration/           # Cross-layer tests (UI + API + DB)
│   └── security/              # SQL injection tests
├── utils/
│   └── helpers.py             # Random data generators, CAPTCHA helper, SQLi payloads
├── conftest.py                # Shared fixtures
├── docker-compose.yml         # Juice Shop container
├── pytest.ini                 # Pytest options and markers
└── requirements.txt
```


## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- Python 3.11+
- Git 

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dkishordev/pytest-juice-shop.git
cd pytest-juice-shop
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
playwright install
```

### 3. Start OWASP Juice Shop

```bash
docker compose up -d
```

The application is served at [http://127.0.0.1:3000](http://127.0.0.1:3000). 

```bash
docker compose ps
```

> The compose file mounts `data/juiceshop.sqlite` into the container, which is how the database tests read the same data the application writes.

## Running the Tests

Run the whole suite:

```bash
pytest
```

Run a single layer:

```bash
pytest -m ui
pytest -m api
pytest -m db
pytest -m integration
pytest -m sqli
```

Run a quick smoke check:

```bash
pytest -m smoke
```

Run in parallel and retry flaky tests:

```bash
pytest -n 4 --reruns 2
```

Run a single file or test:

```bash
pytest tests/api/test_products_api.py
pytest tests/ui/test_login_ui.py::test_ui05_valid_credentials_log_the_user_in
```

## View the report

After a run, open:

```
reports/report.html
```

It's a self-contained HTML file (via `pytest-html`) with pass/fail status,
duration, and captured output per test.

## Tearing down

```powershell
docker compose down -v
```

`-v` also removes the named volume state so the next `up` starts from a
clean seeded database.

## Notes
- Locators/endpoints can differ between Juice Shop versions: use `playwright codegen http://localhost:3000`.
- Run against your own local container only.