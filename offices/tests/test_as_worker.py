import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from companies.models import Company
from offices.models import Office


class OfficeTestCase(TestCase):
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

        self.worker_office = User.objects.create(
            email="worker_office@test.com",
            username="worker_office@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company,
            office=self.office
        )

        self.office_2 = Office.objects.create(
            name="Office 2",
            country="UA",
            region="Lviv Region",
            city="Lviv",
            address="Independence Str.",
            company=self.company
        )

        self.worker_office_2 = User.objects.create(
            email="worker_office_2@test.com",
            username="worker_office_2@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company,
            office=self.office_2
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

        self.worker_office_outside = User.objects.create(
            email="worker_office_outside@test.com",
            username="worker_office_outside@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company_outside,
            office=self.office_outside
        )

        self.token = str(RefreshToken.for_user(self.worker_office).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % (self.token))

    def test_create(self):
        body = {}

        response = self.client.post("/offices/", json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")
        self.assertEqual(Office.objects.all().count(), 3)

    def test_index(self):
        response = self.client.get("/offices/")

        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(json.loads(response.content)[0]["name"], self.office.name)
        self.assertEqual(json.loads(response.content)[1]["name"], self.office_2.name)

    def test_show(self):
        response = self.client.get("/offices/%s/"%(self.office.id))

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")

    def test_show_other_office(self):
        response = self.client.get("/offices/%s/"%(self.office_2.id))

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")

    def test_show_outside(self):
        response = self.client.get("/offices/%s/"%(self.office_outside.id))

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")

    def test_update(self):
        body = {}

        response = self.client.patch("/offices/%s/"%(self.office.id), json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")
        self.assertEqual(Office.objects.get(name=self.office.name).name, self.office.name)

    def test_update_other_office(self):
        body = {}

        response = self.client.patch("/offices/%s/"%(self.office_2.id), json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")
        self.assertEqual(Office.objects.get(name=self.office_2.name).name, self.office_2.name)

    def test_update_outside(self):
        body = {}

        response = self.client.patch("/offices/%s/"%(self.office_outside.id), json.dumps(body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")
        self.assertEqual(Office.objects.get(name=self.office_outside.name).name, self.office_outside.name)

    def test_delete(self):
        response = self.client.delete("/offices/%s/"%(self.office.id))

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")
        self.assertEqual(Office.objects.filter(name=self.office.name).count(), 1)

    def test_delete_other_office(self):
        response = self.client.delete("/offices/%s/"%(self.office_2.id))

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")
        self.assertEqual(Office.objects.filter(name=self.office_2.name).count(), 1)

    def test_delete_outside(self):
        response = self.client.delete("/offices/%s/"%(self.office_outside.id))

        self.assertEqual(json.loads(response.content).get("detail"), "You should be company admin to perform this action.")
        self.assertEqual(Office.objects.filter(name=self.office_outside.name).count(), 1)
