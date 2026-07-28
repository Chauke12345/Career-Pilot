from datetime import date

from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applications.models import JobApplication, ApplicationEvent


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        applications = JobApplication.objects.filter(
            user=request.user
        )

        events = ApplicationEvent.objects.filter(
            application__user=request.user
        ).order_by("date")


        # -----------------------------
        # STATUS SUMMARY
        # -----------------------------

        status_summary = {}

        for status, label in JobApplication.STATUS_CHOICES:

            status_summary[label] = applications.filter(
                status=status
            ).count()


        # -----------------------------
        # APPLICATION METRICS
        # -----------------------------

        total_applications = applications.count()

        interviews = applications.filter(
            status="Interview"
        ).count()

        offers = applications.filter(
            status="Offer"
        ).count()

        rejected = applications.filter(
            status="Rejected"
        ).count()


        success_rate = 0

        if total_applications > 0:
            success_rate = round(
                (offers / total_applications) * 100,
                2
            )


        # -----------------------------
        # RECENT APPLICATIONS
        # -----------------------------

        recent_applications = applications.order_by(
            "-created_at"
        )[:5]


        recent_list = []

        for application in recent_applications:

            recent_list.append({
                "company": application.company,
                "position": application.position,
                "status": application.status,
                "date_applied": application.date_applied,
            })


        # -----------------------------
        # UPCOMING EVENTS
        # -----------------------------

        upcoming_events = []

        for event in events:

            upcoming_events.append({

                "company": event.application.company,

                "event": event.title,

                "date": event.date,

                "notes": event.notes,

            })


        return Response({

            "total_applications": total_applications,

            "interviews": interviews,

            "offers": offers,

            "rejected": rejected,

            "success_rate": f"{success_rate}%",

            "status_summary": status_summary,

            "recent_applications": recent_list,

            "upcoming_events": upcoming_events,

        })