from django.contrib.auth.decorators import login_required
from django.urls import path
from dashboard.views import *

dashboard_urlpatterns = [
    path("dashboard",
         login_required(ApplicantDashboardView.as_view()),
         name="applicant-dashboard"),
    path("staff/dashboard",
         login_required(StaffDashboardView.as_view()),
         name="staff-dashboard"),
]
