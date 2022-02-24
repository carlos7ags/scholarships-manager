from django.contrib.auth.decorators import login_required
from django.urls import path

from applications.views import *

applications_urlpatterns = [
    path("applications",
         login_required(ApplicationsListView.as_view()),
         name="applications-list"),
]
