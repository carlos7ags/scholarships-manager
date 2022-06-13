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
        "staff/awards",
        login_required(AwardsListView.as_view()),
        name="staff-awards-list",
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
        "staff/awards/<pk>/deliver",
        login_required(deliver_award),
        name="staff-deliver-award",
    ),
    path(
        "staff/awards/<pk>/validate",
        login_required(validate_deliverable),
        name="staff-validate-deliverable",
    ),
    path(
        "staff/application/<pk>/award/redirect",
        login_required(ApplicationAwardRedirect.as_view()),
        name="staff-application-award-redirect",
    ),
    path(
        "staff/application/<pk>/award/create",
        login_required(ApplicationAwardCreate.as_view()),
        name="staff-application-award-create",
    ),
    path(
        "staff/application/<pk>/award/update",
        login_required(ApplicationAwardUpdate.as_view()),
        name="staff-application-award-update",
    ),
]
