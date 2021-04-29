from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.db import models
import json


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        data = {
            "username": "mark11a",
            "password": "markweek11",
            "first_name": "Mark",
            "last_name": "Foley"
        }
        get_user_model().objects.create_user(**data)

        print("Ran setUp")

    def test_register_good_user(self):
        url = reverse("register_user")
        data = {
            "username": "mark11b",
            "password": "markweek11",
            "first_name": "test",
            "last_name": "user",
            "is_admin": False
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(url, "/register/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)

        this_user = get_user_model().objects.get(username="mark11b")
        self.assertEqual(this_user.username, 'mark11b')

        print("Ran test_register_good_user")

    def test_register_no_username(self):
        url = reverse("register_user")
        data = {
            "password": "markweek11",
            "first_name": "Mark",
            "last_name": "Foley",
            "is_admin": False
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(url, "/register/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1, "One User added")

        print("Ran test_register_no_username")

    def test_register_no_password(self):
        url = reverse("register_user")
        data = {
            "username": "mark11c",
            "first_name": "Mark",
            "last_name": "Foley",
            "is_admin": False
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(url, "/register/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 1)

        try:
            this_user = get_user_model().objects.get(username="mark11c")
        except get_user_model().DoesNotExist:
            this_user = None
        self.assertFalse(this_user)

        print("Ran test_register_no_password")

    def test_good_login(self):
        url = reverse("login_user")
        data = {
            "username": "mark11a",
            "password": "markweek11"
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.json().get("access") or None
        self.assertTrue(token)

        print("Ran test_good_login")

    def test_bad_login_bad_password(self):
        url = reverse("login_user")
        data = {
            "username": "mark11a",
            "password": "markweek11xxx"
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token = response.json().get("access") or None
        self.assertFalse(token)

        print("Ran test_bad_login_bad_password")

    def test_bad_login_no_password(self):
        url = reverse("login_user")
        data = {
            "username": "mark11a"
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        token = response.json().get("access") or None
        self.assertFalse(token)

        print("Ran test_bad_login_no_password")

    def test_bad_login_no_username(self):
        url = reverse("login_user")
        data = {
            "password": "markweek11"
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        token = response.json().get("access") or None
        self.assertFalse(token)

        print("Ran test_bad_login_no_username")

    def test_get_current_user_ok(self):
        url = reverse("get_current_user_details")

        login_url = reverse("login_user")
        login_data = {
            "username": "mark11a",
            "password": "markweek11"
        }
        response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Assert Login OK")
        token = response.json().get("access") or None

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Assert get user details OK")
        response_user = response.json().get("name") or None
        self.assertEqual(response_user, "Mark Foley")
        self.client.credentials()

        print("Ran test_get_current_user_ok")

    def test_get_current_user_invalid_token(self):
        url = reverse("get_current_user_details")

        bad_token = \
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE5MDI2Nzk1LCJqdGkiOiJmNzM" \
            "1ZGM3NGVhZTU0NjA4OTdiMTU4M2Y4YzljMWI0ZiIsInVzZXJfaWQiOjF9.q5Qq4hi1OqoztKAcH9V_hmsdrWPIZPhk4eNQjXCpERI"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {bad_token}")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials()

        print("Ran test_get_current_user_invalid_token")
