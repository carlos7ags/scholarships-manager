from django.contrib.auth.decorators import login_required
from django.urls import path

from reviews.views import *

reviews_urlpatterns = [
    path(
        "staff/applications",
        login_required(ApplicationsListView.as_view()),
        name="staff-applications-list",
    ),
    path(
        "staff/applications/<pk>",
        login_required(ApplicationDetailReview.as_view()),
        name="staff-application-review",
    ),
    path(
        "staff/applications/<pk>/validate",
        login_required(validate_application),
        name="staff-application-review-validate",
    ),
    path(
        "staff/applications/<pk>/comment",
        login_required(comment_application),
        name="staff-application-review-comment",
    ),
    path(
        "staff/program/<program_id>/application/<application_id>/award/redirect",
        login_required(ApplicationAwardRedirect),
        name="staff-application-award-redirect",
    ),
    path(
        "staff/program/<program_id>/application/<application_id>/award/create",
        login_required(ApplicationAwardCreate),
        name="staff-application-award-create",
    ),
    path(
        "staff/program/<program_id>/application/<application_id>/award/<pk>/update",
        login_required(ApplicationAwardUpdate),
        name="staff-application-award-update",
    ),
]
