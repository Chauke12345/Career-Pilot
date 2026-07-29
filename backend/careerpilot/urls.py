"""
URL configuration for careerpilot project.
"""

from django.contrib import admin
from django.urls import path, include

from pages import views

from django.conf import settings
from django.conf.urls.static import static


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)



urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        "admin/",
        admin.site.urls
    ),



    # =========================
    # JWT AUTHENTICATION
    # =========================

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),


    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),



    # =========================
    # API ROUTES
    # =========================


    path(
        "api/accounts/",
        include("accounts.urls")
    ),


    path(
        "api/profile/",
        include("profiles.urls")
    ),


    path(
        "api/applications/",
        include("applications.urls")
    ),


    path(
        "api/dashboard/",
        include("dashboard.urls")
    ),


    path(
        "api/ai/",
        include("ai_tools.urls")
    ),



    # =========================
    # RESUME QUALITY ANALYZER
    # =========================

    path(
        "api/resume/",
        include("resume.urls")
    ),
    path(
    "api/matching/",
    include("matching.urls")
),



    # =========================
    # CAREER ASSISTANT
    # =========================

    path(
        "assistant/",
        include("assistant.urls")
    ),



    # =========================
    # API DOCUMENTATION
    # =========================

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),


    path(
        "swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),



    # =========================
    # FRONTEND PAGES
    # =========================

    path(
        "",
        views.home,
        name="home"
    ),


    path(
        "login/",
        views.login_page,
        name="login"
    ),


    path(
        "signup/",
        views.signup,
        name="signup"
    ),


    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    path(
        "applications/",
        views.applications,
        name="applications"
    ),

]



# =========================
# STATIC FILES DEVELOPMENT
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )