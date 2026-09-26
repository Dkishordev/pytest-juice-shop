"""
Thin wrapper around Juice Shop's REST/GraphQL-free JSON API. Used both by
API-level security tests directly, and by UI tests to set up state quickly
(e.g. registering a user via API instead of clicking through the form).

Endpoints reflect the actual Juice Shop app (v14+). Adjust paths if you're
targeting a fork with a different API surface.
"""
from __future__ import annotations
import requests
from config.settings import settings


class APIClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or settings.API_BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.token: str | None = None

    # --- auth -----------------------------------------------------------

    def register(self, email: str, password: str, security_answer: str = "blue") -> requests.Response:
        payload = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {"id": 1, "question": "Your eye color?", "createdAt": "", "updatedAt": ""},
            "securityAnswer": security_answer,
        }
        return self.session.post(f"{self.base_url}/api/Users", json=payload)

    def login(self, email: str, password: str) -> requests.Response:
        resp = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": email, "password": password},
        )
        if resp.status_code == 200:
            token = resp.json().get("authentication", {}).get("token")
            if token:
                self.token = token
                self.session.headers.update({"Authorization": f"Bearer {token}"})
        return resp

    def logout(self):
        self.token = None
        self.session.headers.pop("Authorization", None)

    def whoami(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/rest/user/whoami")

    # --- products / search ------------------------------------------------

    def get_products(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/rest/products")

    def search_products(self, query: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/rest/products/search", params={"q": query})

    def get_product(self, product_id: int) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/Products/{product_id}")

    def update_product(self, product_id: int, data: dict) -> requests.Response:
        # Intentionally used to test whether a non-admin can update pricing (mass assignment / BAC).
        return self.session.put(f"{self.base_url}/api/Products/{product_id}", json=data)

    # --- basket / checkout --------------------------------------------------

    def get_basket(self, basket_id: int) -> requests.Response:
        return self.session.get(f"{self.base_url}/rest/basket/{basket_id}")

    def add_to_basket(self, product_id: int, quantity: int, basket_id: int = 1) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/BasketItems",
            json={"ProductId": product_id, "BasketId": basket_id, "quantity": quantity},
        )

    def apply_coupon(self, basket_id: int, coupon: str) -> requests.Response:
        return self.session.put(f"{self.base_url}/rest/basket/{basket_id}/coupon/{coupon}")

    # --- feedback / reviews -----------------------------------------------

    def submit_feedback(self, comment: str, rating: int = 5) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/Feedbacks", json={"comment": comment, "rating": rating}
        )

    def submit_review(self, product_id: int, message: str) -> requests.Response:
        return self.session.put(
            f"{self.base_url}/rest/products/{product_id}/reviews", json={"message": message}
        )

    # --- admin / user management --------------------------------------------

    def list_users(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/Users")

    def get_user(self, user_id: int) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/Users/{user_id}")

    def get_security_questions(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/SecurityQuestions")

    # --- misc endpoints used by access-control / info-disclosure tests -------

    def get_metrics(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/metrics")

    def get_admin_application_version(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/rest/admin/application-version")

    def raw_get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def raw_post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(f"{self.base_url}{path}", **kwargs)
