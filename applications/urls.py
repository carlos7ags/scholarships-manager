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
        "program/<program_id>/application/<application_id>/form/redirect",
        login_required(ApplicationFormRedirect.as_view()),
        name="application-form-redirect",
    ),
    path(
        "application/<pk>/form/apoyo",
        login_required(ApplicationFormApoyoCreate.as_view()),
        name="application-form-apoyo-create",
    ),
    path(
        "application/<pk>/form/convocatoria",
        login_required(ApplicationFormConvocatoriaCreate.as_view()),
        name="application-form-convocatoria-create",
    ),
    path(
        "application/<pk>/form/apoyo/update",
        login_required(ApplicationFormApoyoUpdate.as_view()),
        name="application-form-apoyo-update",
    ),
    path(
        "application/<pk>/form/convocatoria/update",
        login_required(ApplicationFormConvocatoriaUpdate.as_view()),
        name="application-form-convocatoria-update",
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
    path(
        "application/<application_id>/task/<task_id>/update",
        login_required(update_application),
        name="update-application",
    ),
    path(
        "application/<pk>/completionproof",
        login_required(upload_final_proof),
        name="upload-final-proof",
    ),
]
