import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from companies.models import Company
from offices.models import Office
from vehicles.models import Vehicle


class OfficeTestCase(TestCase):
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

        self.office = Office.objects.create(
            name="Office",
            country="UA",
            region="Lviv Region",
            city="Lviv",
            address="Independence Str.",
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

        self.vehicle = Vehicle.objects.create(
            name="Vehicle",
            model="model_x",
            license_plate="abc123",
            year_of_manufacture="2023",
            office=self.office
        )

        self.vehicle_2 = Vehicle.objects.create(
            name="Vehicle 2",
            model="model_x",
            license_plate="abc123",
            year_of_manufacture="2023",
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

        self.vehicle_outside = Vehicle.objects.create(
            name="Vehicle",
            model="model_x",
            license_plate="abc123",
            year_of_manufacture="2023",
            office=self.office_outside
        )

        self.token = str(RefreshToken.for_user(self.admin).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % (self.token))

    # def test_create(self):
    #     body = {
    #         "name": "Vehicle 3",
    #         "model": "model_x",
    #         "license_plate": "abc123",
    #         "year_of_manufacture": "2023",
    #         "office": self.office.id
    #     }

    #     response = self.client.post("/vehicles/", json.dumps(body), content_type="application/json")

    #     self.assertEqual(json.loads(response.content)["name"], body["name"])
    #     self.assertEqual(Vehicle.objects.filter(name=body["name"]).count(), 1)
    #     self.assertEqual(Vehicle.objects.get(name=body["name"]).company, self.company)
    #     self.assertEqual(Vehicle.objects.get(name=body["name"]).office, self.office)

    # def test_create_with_invalid_params(self):
    #     body = {
    #         "name": "",
    #         "model": "",
    #         "license_plate": "",
    #         "year_of_manufacture": 0,
    #         "office": self.office_outside.id
    #     }

    #     response = self.client.post("/vehicles/", json.dumps(body), content_type="application/json")

    #     self.assertEqual(json.loads(response.content)["name"], ['This field may not be blank.'])
    #     self.assertEqual(json.loads(response.content)["model"], ['This field may not be blank.'])
    #     self.assertEqual(json.loads(response.content)["license_plate"], ['This field may not be blank.'])
    #     self.assertIn("Ensure this value is greater than or equal to", json.loads(response.content)["year_of_manufacture"][0])
    #     # self.assertEqual(json.loads(response.content)["office"], "Not found.")
    #     self.assertEqual(Vehicle.objects.all().count(), 3)

    # def test_create_with_no_params(self):
    #     body = {}

    #     response = self.client.post("/offices/", json.dumps(body), content_type="application/json")

    #     self.assertEqual(response.content, b'{"name":["This field is required."],"country":["This field is required."],"region":["This field is required."],"city":["This field is required."],"address":["This field is required."]}')
    #     self.assertEqual(Office.objects.all().count(), 3)

    # def test_index(self):
    #     response = self.client.get("/offices/")

    #     self.assertEqual(len(json.loads(response.content)), 2)
    #     self.assertEqual(json.loads(response.content)[0]["name"], self.office.name)
    #     self.assertEqual(json.loads(response.content)[1]["name"], self.office_2.name)

    # def test_show(self):
    #     response = self.client.get("/offices/%s/"%(self.office.id))

    #     self.assertEqual(json.loads(response.content)["name"], self.office.name)

    # def test_show_outside(self):
    #     response = self.client.get("/offices/%s/"%(self.office_outside.id))

    #     self.assertEqual(json.loads(response.content)["detail"], "Not found.")

    # def test_update(self):
    #     body = {
    #         "name": "new_name",
    #         "country": "new_country",
    #         "region": "new_region",
    #         "city": "new_city",
    #         "address": "new_address"
    #     }

    #     response = self.client.patch("/offices/%s/"%(self.office.id), json.dumps(body), content_type="application/json")

    #     self.assertEqual(json.loads(response.content)["name"], body["name"])
    #     self.assertEqual(Office.objects.get(pk=self.office.id).name, body["name"])
    #     self.assertEqual(Office.objects.get(pk=self.office.id).address, body["address"])

    # def test_update_outside(self):
    #     body = {
    #         "name": "new_name",
    #         "country": "new_country",
    #         "region": "new_region",
    #         "city": "new_city",
    #         "address": "new_address"
    #     }

    #     response = self.client.patch("/offices/%s/"%(self.office_outside.id), json.dumps(body), content_type="application/json")

    #     self.assertEqual(json.loads(response.content).get("detail"), "Not found.")
    #     self.assertEqual(Office.objects.get(pk=self.office_outside.id).name, self.office_outside.name)
    #     self.assertEqual(Office.objects.get(pk=self.office_outside.id).address, self.office_outside.address)

    # def test_delete(self):
    #     response = self.client.delete("/offices/%s/"%(self.office.id))

    #     self.assertEqual(response.content, b'')
    #     self.assertEqual(Office.objects.filter(name=self.office.name).count(), 0)

    # def test_delete_outside(self):
    #     response = self.client.delete("/offices/%s/"%(self.office_outside.id))

    #     self.assertEqual(json.loads(response.content).get("detail"), "Not found.")
    #     self.assertEqual(Office.objects.filter(name=self.office_outside.name).count(), 1)
