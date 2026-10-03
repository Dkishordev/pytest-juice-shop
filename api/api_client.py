import requests
from config.settings import settings


class APIClient:

    def __init__(self, base_url=None):
        self.base_url = (base_url or settings.API_BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.token = None

    # Login and user account

    def register(self, email, password, security_answer="blue"):
        data = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {
                "id": 1,
                "question": "Your eye color?",
                "createdAt": "",
                "updatedAt": ""
            },
            "securityAnswer": security_answer
        }

        return self.session.post(
            self.base_url + "/api/Users",
            json=data
        )

    def login(self, email, password):
        data = {
            "email": email,
            "password": password
        }

        response = self.session.post(
            self.base_url + "/rest/user/login",
            json=data
        )

        if response.status_code == 200:
            token = response.json().get("authentication", {}).get("token")

            if token:
                self.token = token
                self.session.headers["Authorization"] = "Bearer " + token

        return response

    def logout(self):
        self.token = None

        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

    def whoami(self):
        return self.session.get(
            self.base_url + "/rest/user/whoami"
        )

    # Products

    def get_products(self):
        return self.session.get(
            self.base_url + "/rest/products/search"
        )

    def search_products(self, query):
        return self.session.get(
            self.base_url + "/rest/products/search",
            params={"q": query}
        )

    def get_product(self, product_id):
        return self.session.get(
            self.base_url + "/api/Products/" + str(product_id)
        )

    def update_product(self, product_id, data):
        return self.session.put(
            self.base_url + "/api/Products/" + str(product_id),
            json=data
        )

    # Basket

    def get_basket(self, basket_id):
        return self.session.get(
            self.base_url + "/rest/basket/" + str(basket_id)
        )

    def add_to_basket(self, product_id, quantity, basket_id=1):
        data = {
            "ProductId": product_id,
            "BasketId": basket_id,
            "quantity": quantity
        }

        return self.session.post(
            self.base_url + "/api/BasketItems",
            json=data
        )

    def apply_coupon(self, basket_id, coupon):
        return self.session.put(
            self.base_url + "/rest/basket/" + str(basket_id) + "/coupon/" + coupon
        )

    # Feedback and reviews

    def submit_feedback(self, comment, rating=5):
        data = {
            "comment": comment,
            "rating": rating
        }

        return self.session.post(
            self.base_url + "/api/Feedbacks",
            json=data
        )

    def submit_review(self, product_id, message):
        return self.session.put(
            self.base_url + "/rest/products/" + str(product_id) + "/reviews",
            json={"message": message}
        )

    # Users

    def list_users(self):
        return self.session.get(
            self.base_url + "/api/Users"
        )

    def get_user(self, user_id):
        return self.session.get(
            self.base_url + "/api/Users/" + str(user_id)
        )

    def get_security_questions(self):
        return self.session.get(
            self.base_url + "/api/SecurityQuestions"
        )

    # Other endpoints

    def get_metrics(self):
        return self.session.get(
            self.base_url + "/metrics"
        )

    def get_admin_application_version(self):
        return self.session.get(
            self.base_url + "/rest/admin/application-version"
        )

    def raw_get(self, path, **kwargs):
        return self.session.get(
            self.base_url + path,
            **kwargs
        )

    def raw_post(self, path, **kwargs):
        return self.session.post(
            self.base_url + path,
            **kwargs
        )
