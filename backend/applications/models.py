from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Screening", "Screening"),
        ("Interview", "Interview"),
        ("Technical Test", "Technical Test"),
        ("Offer", "Offer"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    company = models.CharField(
        max_length=100
    )

    position = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    job_link = models.URLField(
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    date_applied = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.position} - {self.company}"



class ApplicationEvent(models.Model):

    EVENT_STATUS_MAP = {
        "Applied": "Applied",
        "Screening": "Screening",
        "Interview": "Interview",
        "Technical Test": "Technical Test",
        "Offer": "Offer",
        "Rejected": "Rejected",
    }

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(
        max_length=100
    )

    date = models.DateField()

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def save(self, *args, **kwargs):

        for event, status in self.EVENT_STATUS_MAP.items():

            if event.lower() in self.title.lower():

                self.application.status = status
                self.application.save()

                break

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} - {self.application.company}"