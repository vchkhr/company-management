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
            username="admin@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company
        )
        self.company.admin = self.admin
        self.company.save()

        self.worker = User.objects.create(
            email="worker@test.com",
            username="worker@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
            company=self.company
        )

        self.admin_outside = User.objects.create(
            email="admin_outside@test.com",
            username="admin_outside@test.com",
            first_name="first",
            last_name="last",
            password="test_password_123",
        )

        self.token = str(RefreshToken.for_user(self.admin).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % (self.token))

    def test_create(self):
        worker_body = {
            "email": "worker2@test.com",
            "username": "worker2@test.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "password": "test_password_123"
        }

        response = self.client.post("/users/", json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["email"], worker_body["email"])
        self.assertEqual(User.objects.filter(email=worker_body["email"]).count(), 1)

    def test_create_duplicate(self):
        worker_body = {
            "email": "worker@test.com",
            "username": "worker2@test.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "password": "test_password_123"
        }

        response = self.client.post("/users/", json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["email"], ["user with this email address already exists."])
        self.assertEqual(User.objects.all().count(), 3)

    def test_index(self):
        response = self.client.get("/users/")

        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(json.loads(response.content)[0]["email"], self.admin.email)
        self.assertEqual(json.loads(response.content)[1]["email"], self.worker.email)

    def test_show_admin(self):
        response = self.client.get("/users/%s/" % (self.admin.id))

        self.assertEqual(json.loads(response.content)["email"], self.admin.email)

    def test_show_worker(self):
        response = self.client.get("/users/%s/" % (self.worker.id))

        self.assertEqual(json.loads(response.content)["email"], self.worker.email)

    def test_update_worker(self):
        worker_body = {
            "first_name": "New first name",
            "last_name": "New last name",
            "password": "new_password_123"
        }

        response = self.client.patch("/users/%s/" % (self.worker.id), json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["first_name"], worker_body["first_name"])
        self.assertEqual(User.objects.get(email=self.worker.email).first_name, worker_body["first_name"])
        self.assertEqual(User.objects.get(email=self.worker.email).last_name, worker_body["last_name"])

    def test_update_admin_outside(self):
        original_first_name = self.admin_outside.first_name

        admin_outside_body = {
            "first_name": "New first name",
            "last_name": "New last name",
            "password": "new_password_123"
        }

        response = self.client.patch("/users/%s/" % (self.admin_outside.id), json.dumps(admin_outside_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["detail"], "Not found.")
        self.assertEqual(self.admin_outside.first_name, original_first_name)

    def test_update_worker_email(self):
        worker_body = {
            "email": "new@test.com"
        }

        response = self.client.patch("/users/%s/" % (self.worker.id), json.dumps(worker_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["email"], self.worker.email)
        self.assertEqual(User.objects.filter(email=self.worker.email).count(), 1)

    def test_delete_worker(self):
        response = self.client.delete("/users/%s/" % (self.worker.id))

        self.assertEqual(response.content, b'')
        self.assertEqual(User.objects.filter(email=self.worker.email).count(), 0)

    def test_delete_admin(self):
        response = self.client.delete("/users/%s/" % (self.admin.id))

        self.assertEqual(response.content, b'')
        self.assertEqual(User.objects.filter(email=self.admin.email).count(), 0)
        self.assertEqual(User.objects.filter(email=self.worker.email).count(), 0)
        self.assertEqual(Company.objects.filter(admin=self.admin).count(), 0)

    def test_delete_admin_outside(self):
        response = self.client.delete("/users/%s/" % (self.admin_outside.id))

        self.assertEqual(json.loads(response.content)["detail"], "Not found.")
        self.assertEqual(User.objects.filter(email=self.admin_outside.email).count(), 1)
