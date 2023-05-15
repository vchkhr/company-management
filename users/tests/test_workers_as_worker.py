import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from companies.models import Company


class UserTestCase(TestCase):
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

        self.worker2 = User.objects.create(
            email="worker2@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company
        )

        self.token = str(RefreshToken.for_user(self.worker).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s"%(self.token))

    def test_create(self):
        worker_body = {
            "email": "worker2@test.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "password": "test_password_123"
        }

        response = self.client.post(
            "/users/", json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")

    def test_index(self):
        response = self.client.get("/users/")

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")

    def test_show_admin(self):
        response = self.client.get("/users/%s/" % (self.admin.id))

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")

    def test_show_other_worker(self):
        response = self.client.get("/users/%s/" % (self.worker2.id))

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")

    def test_show(self):
        response = self.client.get("/users/%s/" % (self.worker.id))

        self.assertEqual(json.loads(response.content)["email"], self.worker.email)

    def test_update_other_worker(self):
        worker_body = {
            "first_name": "New first name",
            "last_name": "New last name",
            "password": "new_password_123"
        }

        response = self.client.patch("/users/%s/" % (self.worker2.id), json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")

    def test_update(self):
        worker_body = {
            "first_name": "New first name",
            "last_name": "New last name",
            "password": "new_password_123"
        }

        response = self.client.patch("/users/%s/" % (self.worker.id), json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("first_name"), worker_body["first_name"])

    def test_update_email(self):
        worker_body = {
            "email": "new@test.com"
        }

        response = self.client.patch("/users/%s/" % (self.worker.id), json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content).get("email"), self.worker.email)

    def test_delete_other_worker(self):
        response = self.client.delete("/users/%s/" % (self.worker2.id))

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")

    def test_delete(self):
        response = self.client.delete("/users/%s/" % (self.worker.id))

        self.assertEqual(json.loads(response.content)["detail"], "You should be company admin to perform this action.")
