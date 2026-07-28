from django.contrib import admin
from .models import JobApplication, ApplicationEvent


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "position",
        "status",
        "user",
        "date_applied",
    )

    list_filter = (
        "status",
        "date_applied",
    )

    search_fields = (
        "company",
        "position",
        "user__username",
    )


@admin.register(ApplicationEvent)
class ApplicationEventAdmin(admin.ModelAdmin):

    list_display = (
        "application",
        "title",
        "date",
    )

    list_filter = (
        "date",
        "title",
    )