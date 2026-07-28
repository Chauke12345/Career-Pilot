from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from applications.models import JobApplication, ApplicationEvent


class DashboardAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="dashboarduser",
            password="password123"
        )

        self.client.force_authenticate(
            user=self.user
        )


    def test_dashboard_returns_data(self):

        JobApplication.objects.create(
            user=self.user,
            company="Microsoft",
            position="Python Developer",
            status="Interview"
        )


        response = self.client.get(
            "/api/dashboard/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


        self.assertEqual(
            response.data["total_applications"],
            1
        )


        self.assertEqual(
            response.data["interviews"],
            1
        )


    def test_dashboard_requires_authentication(self):

        self.client.logout()


        response = self.client.get(
            "/api/dashboard/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )