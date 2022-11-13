from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.forms import RedactorCreationForm, RedactorExperienceUpdateForm
from catalog.models import Topic


class FormsTests(TestCase):
    def test_redactor_creation_form(self):
        form_data = {
            "username": "test_user",
            "password1": "user1234",
            "password2": "user1234",
            "years_of_experience": 10,
            "first_name": "Jason",
            "last_name": "Statham",
        }

        form = RedactorCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_redactor_update_form(self):
        form_data = {"years_of_experience": 5}

        form = RedactorExperienceUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TopicModelTest(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), topic.name)


class PublicDriverTests(TestCase):
    def test_login_required_redactor_list(self):
        res = self.client.get(reverse("catalog:redactor-list"))

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_redactor_detail(self):
        user = get_user_model().objects.create_user(
            username="test", password="test12345", years_of_experience=5
        )
        res = self.client.get(
            reverse("catalog:redactor-detail", args=[user.id])
        )

        self.assertNotEqual(res.status_code, 200)


class PrivateRedactorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="password1234", years_of_experience=3
        )
        self.client.force_login(self.user)

    def test_redactor_list(self):
        self.user = get_user_model().objects.create_user(
            username="IVAN", password="qwerty123", years_of_experience=6
        )
        redactors = get_user_model().objects.all()
        res = self.client.get(reverse("catalog:redactor-list"))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["redactor_list"]), list(redactors))
        self.assertTemplateUsed(res, "catalog/redactor_list.html")

    def test_driver_detail(self):
        res = self.client.get(reverse(
            "catalog:redactor-detail",
            args=[self.user.id])
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["redactor"], self.user)
        self.assertTemplateUsed(res, "catalog/redactor_detail.html")

    def test_redactor_create(self):
        form_data = {
            "username": "test",
            "password1": "password1234",
            "password2": "password1234",
            "first_name": "Ivan",
            "last_name": "Drago",
            "years_of_experience": 3,
        }
        self.client.post(reverse("catalog:redactor-create"), data=form_data)
        user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(
            user.years_of_experience, form_data["years_of_experience"]
        )
