from django.contrib.auth.decorators import login_required
from django.urls import path

from applications.views import *

applications_urlpatterns = [
    path(
        "program/<id>/application",
        login_required(create_application),
        name="create-application",
    ),
]
