from django.contrib.auth.decorators import login_required
from django.urls import path

from programs.views import *

programs_urlpatterns = [
    path("programs", login_required(ProgramsListView.as_view()), name="programs-list"),
]
