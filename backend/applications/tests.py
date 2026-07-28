from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from .models import JobApplication, ApplicationEvent


class JobApplicationAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.client.force_authenticate(
            user=self.user
        )


    def test_create_job_application(self):

        data = {
            "company": "Google",
            "position": "Backend Developer",
            "location": "Remote",
            "status": "Applied",
            "job_link": "https://google.com",
            "notes": "Test application"
        }


        response = self.client.post(
            "/api/applications/",
            data
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


        self.assertEqual(
            JobApplication.objects.count(),
            1
        )


        self.assertEqual(
            JobApplication.objects.first().company,
            "Google"
        )


    def test_user_only_sees_own_applications(self):

        JobApplication.objects.create(
            user=self.user,
            company="OpenAI",
            position="Python Developer"
        )


        response = self.client.get(
            "/api/applications/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


        self.assertEqual(
            response.data["count"],
            1
        )



class ApplicationEventAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="eventuser",
            password="password123"
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.application = JobApplication.objects.create(
            user=self.user,
            company="OpenAI",
            position="Backend Developer",
            status="Interview"
        )


    def test_create_application_event(self):

        data = {
            "title": "Technical Interview",
            "date": "2026-08-01",
            "notes": "Prepare Django REST Framework"
        }


        response = self.client.post(
            f"/api/applications/{self.application.id}/events/",
            data
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


        self.assertEqual(
            ApplicationEvent.objects.count(),
            1
        )


        self.assertEqual(
            ApplicationEvent.objects.first().title,
            "Technical Interview"
        )