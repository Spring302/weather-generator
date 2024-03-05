from django.test import TestCase
from django.utils import timezone

from .utils.utils import *
from .views import *
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model


class LoginAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser("template", "admin@myproject.com", "template")

    def test_login_access_with_future_record(self):
        future_time = {"check_time": str(timezone.now() + timedelta(days=1))}
        self.assertTrue(is_record_future_time(future_time))

    def test_login_access_with_recent_record(self):
        recent_time = {"check_time": str(timezone.now())}
        self.assertFalse(is_record_future_time(recent_time))

    def test_login_access_with_old_record(self):
        old_time = {"check_time": str(timezone.now() - timedelta(days=1))}
        self.assertFalse(is_record_future_time(old_time))


    def test_post_list(self):
        # Using the standard RequestFactory API to create a form POST request
        factory = APIRequestFactory()
        request = factory.post("/login/", {"user_id": 1, "tag": "IN"})
        view = LoginAccess.as_view()
        User = get_user_model()
        user = User.objects.get(username="template")
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
