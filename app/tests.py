from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from .models import Snippet


class TestSnippetsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = get_user_model().objects.create_user(
            username="test", password="test"
        )
        response = cls.client.post(
            "/token/", data={"username": "test", "password": "test"}
        )
        access_token = response.json()["access"]
        cls.headers = {"Authorization": "Bearer " + access_token}

    def test_entry_view(self):
        response = self.client.get(reverse("entry_view"))
        assert response.status_code == 200

    def test_snippets_view(self):
        response = self.client.get(reverse("snippets"))
        assert response.status_code == 200

    def test_snippet_create(self):
        data = {"title": "test_title", "code": "test_code"}
        response = self.client.post(
            reverse("snippets"), data=data, headers=self.headers
        )
        assert response.status_code == 201
        assert response.json()["title"] == "test_title"

    def test_registration_endpoint_for_user(self):
        data = {
            "username": "test_user",
            "email": "test_user@gmail.com",
            "password1": "adminiscool",
            "password2": "adminiscool",
        }
        response = self.client.post("/auth/registration/", data=data)

        assert response.status_code == 201

    def test_snippet_detail_view(self):
        data = {"title": "test_title", "code": "test_code"}
        _response = self.client.post(
            reverse("snippets"), data=data, headers=self.headers
        )
        snippet_id = _response.json()["id"]
        response = self.client.get(reverse("snippet_detail", kwargs={"pk": snippet_id}))
        assert response.status_code == 401
        response1 = self.client.get(
            reverse("snippet_detail", kwargs={"pk": snippet_id}), headers=self.headers
        )
        assert response1.status_code == 200
        assert response1.json()["title"] == "test_title"

    def test_snippet_create_with_view_once(self):
        data = {"title": "test_title", "code": "test_code", "view_once": "true"}
        response1 = self.client.post(
            reverse("snippets"), headers=self.headers, data=data
        )
        assert response1.status_code == 201
        snippet_id = response1.json()["id"]
        response = self.client.get(
            reverse("highlight", kwargs={"pk": snippet_id}), headers=self.headers
        )
        assert response.status_code == 200

        response2 = self.client.get(
            reverse("highlight", kwargs={"pk": snippet_id}), headers=self.headers
        )
        assert response2.status_code == 204
        response3 = self.client.get(
            reverse("snippet_detail", kwargs={"pk": snippet_id}), headers=self.headers
        )
        print(response3.json())
        assert response3.status_code == 404

    def test_snippet_with_password(self):
        data = {"title": "test_title", "code": "test_code", "password": "test1"}
        response = self.client.post(
            reverse("snippets"), headers=self.headers, data=data
        )
        assert response.status_code == 201
        snippet_id = response.json()["id"]
        data1 = {"password": "test1"}
        response1 = self.client.post(
            reverse("password-required", kwargs={"pk": snippet_id}),
            headers=self.headers,
            data=data1,
        )
        assert response1.status_code == 200
        password_token = response1.json()["password_token"]
        jwt_token = self.headers["Authorization"]
        headers = {"Authorization": jwt_token, "X-Access-Token": password_token}
        response3 = self.client.get(
            reverse("snippet_detail", kwargs={"pk": snippet_id}), headers=headers
        )
        assert response3.status_code == 200
        assert response3.json()["title"] == "test_title"
