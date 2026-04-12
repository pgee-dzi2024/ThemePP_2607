from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Analysis


class MainViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass12345")
        self.client.login(username="testuser", password="pass12345")

    def test_index_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)

    def test_upload_invalid_extension_shows_error(self):
        fake_file = SimpleUploadedFile(
            "data.txt",
            b"some content",
            content_type="text/plain"
        )
        response = self.client.post(reverse("index"), {"datafile": fake_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неподдържан формат")

    def test_upload_csv_creates_analysis(self):
        csv_content = (
            "category,value\n"
            "A,10\n"
            "B,20\n"
            "C,30\n"
        ).encode("utf-8")

        csv_file = SimpleUploadedFile(
            "sales.csv",
            csv_content,
            content_type="text/csv"
        )

        response = self.client.post(reverse("index"), {"datafile": csv_file})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Analysis.objects.filter(user=self.user).count(), 1)
        analysis = Analysis.objects.filter(user=self.user).latest("created_at")
        self.assertEqual(analysis.filename, "sales.csv")
        self.assertAlmostEqual(analysis.total, 60.0, places=2)
        self.assertAlmostEqual(analysis.average, 20.0, places=2)

    def test_history_shows_user_analyses(self):
        Analysis.objects.create(
            user=self.user,
            filename="manual.csv",
            total=100.0,
            average=25.0
        )

        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "manual.csv")

        analyses = response.context["analyses"]
        self.assertEqual(analyses.count(), 1)
        self.assertAlmostEqual(analyses[0].total, 100.0, places=2)

    def test_register_creates_user(self):
        self.client.logout()
        response = self.client.post(
            reverse("register"),
            {"username": "newuser", "password": "newpass123"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())