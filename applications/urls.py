from django.contrib.auth.decorators import login_required
from django.urls import path

from applications.views import *

applications_urlpatterns = [
    path(
        "program/<program_id>/application/new",
        login_required(create_application),
        name="create-application",
    ),
    path(
        "application/<pk>/form",
        login_required(RenderApplicationFormView.as_view()),
        name="render-application-form",
    ),
    path(
        "application/<pk>/form/create",
        login_required(create_application_form),
        name="create-application-form",
    ),
    path(
        "application/<pk>",
        login_required(ApplicationDetailView.as_view()),
        name="application-detail",
    ),
    path(
        "application/<pk>/download",
        login_required(download_application),
        name="application-download",
    ),
    path(
        "application/<pk>/withdraw",
        login_required(withdraw_application),
        name="withdraw-application",
    ),
]
