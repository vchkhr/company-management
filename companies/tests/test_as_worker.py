import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from companies.models import Company


class CompanyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.company = Company.objects.create(name="test")
        self.admin = User.objects.create(
            email="admin@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company
        )
        self.company.admin = self.admin
        self.company.save()

        self.worker = User.objects.create(
            email="worker@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company
        )

        self.token = str(RefreshToken.for_user(self.worker).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % (self.token))

    def test_show(self):
        response = self.client.get("/user/company/")

        self.assertEqual(json.loads(response.content)["name"], self.company.name)

    def test_update(self):
        body = {
            "name": "new_name",
            "address": "new_address"
        }

        response = self.client.patch("/user/company/", json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")
        self.assertEqual(Company.objects.get(pk=self.company.id).name, self.company.name)
        self.assertEqual(Company.objects.get(pk=self.company.id).address, self.company.address)
