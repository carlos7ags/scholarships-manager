from django.contrib.auth.decorators import login_required
from django.urls import path
from reviews.views import *

reviews_urlpatterns = [
    path("staff/applications",
         login_required(ApplicationsListView.as_view()),
         name="staff-applications-list"
         ),
    path("staff/applications/<pk>",
         login_required(ApplicationsListView.as_view()),
         name="staff-application-review"
         ),
]
