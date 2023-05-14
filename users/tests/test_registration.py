import json
from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    admin_body = {
        "email": "admin@test.com",
        "first_name": "first_name",
        "last_name": "last_name",
        "password": "test_password_123",
        "company": {
            "name": "Test"
        }
    }

    def test_registration(self):
        response = self.client.post('/register/', json.dumps(self.admin_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["email"], self.admin_body["email"])
        self.assertEqual(User.objects.filter(email=self.admin_body["email"]).count(), 1)

    def test_registration_with_same_email(self):
        self.client.post('/register/', json.dumps(self.admin_body),content_type="application/json")
        response = self.client.post('/register/', json.dumps(self.admin_body), content_type="application/json")

        self.assertEqual(json.loads(response.content)["email"], ["This field must be unique."])
        self.assertEqual(User.objects.all().count(), 1)

    def test_registration_with_incorrect_values(self):
        response = self.client.post('/register/', json.dumps(
            {
                "email": "admin",
                "first_name": "",
                "last_name": "",
                "password": "",
                "company": {
                    "name": ""
                }
            }
        ), content_type="application/json")

        self.assertEqual(json.loads(response.content),
                         {
            "password": [
                "This field may not be blank."
            ],
            "email": [
                "Enter a valid email address."
            ],
            "company": {
                "name": [
                    "This field may not be blank."
                ]
            }
        }
        )
        self.assertEqual(User.objects.all().count(), 0)

    def test_registration_with_no_values(self):
        response = self.client.post('/register/', json.dumps(
            {}
        ), content_type="application/json")

        self.assertEqual(json.loads(response.content),
                         {
            "password": [
                "This field is required."
            ],
            "email": [
                "This field is required."
            ],
            "first_name": [
                "This field is required."
            ],
            "last_name": [
                "This field is required."
            ],
            "company": [
                "This field is required."
            ]
        }
        )
        self.assertEqual(User.objects.all().count(), 0)
