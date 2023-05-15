import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from companies.models import Company
from offices.models import Office


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.company = Company.objects.create(name="test")
        self.admin = User.objects.create(
            email="admin@test.com",
            username="admin@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company
        )
        self.company.admin = self.admin
        self.company.save()

        self.office = Office.objects.create(
            name="Office",
            country="UA",
            region="Lviv Region",
            city="Lviv",
            address="Independence Str.",
            company=self.company
        )

        self.worker = User.objects.create(
            email="worker@test.com",
            username="worker@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company
        )

        self.office_2 = Office.objects.create(
            name="Office 2",
            country="UA",
            region="Lviv Region",
            city="Lviv",
            address="Independence Str.",
            company=self.company
        )

        self.company_outside = Company.objects.create(name="Company Outside")

        self.office_outside = Office.objects.create(
            name="Office Outside",
            country="UA",
            region="Lviv Region",
            city="Lviv",
            address="Independence Str.",
            company=self.company_outside
        )

        self.token = str(RefreshToken.for_user(self.admin).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % (self.token))

    def test_assign_worker_to_office(self):
        body = {
            "office": self.office.id
        }

        response = self.client.patch("/users/%s/"%(self.worker.id), json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("office"), body["office"])
        self.assertEqual(User.objects.get(pk=self.worker.id).office.id, body["office"])

    def test_assign_worker_to_office_2(self):
        body = {
            "office": self.office_2.id
        }

        response = self.client.patch("/users/%s/"%(self.worker.id), json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("office"), body["office"])
        self.assertEqual(User.objects.get(pk=self.worker.id).office.id, body["office"])


    def test_assign_worker_to_office_outside(self):
        body = {
            "office": self.office_outside.id
        }

        response = self.client.patch("/users/%s/"%(self.worker.id), json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("office"), ["Not found."])
        self.assertEqual(User.objects.get(pk=self.worker.id).office, self.worker.office)
