from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from accounts.urls import accounts_urlpatterns
from profile.urls import profile_urlpatterns
from dashboard.urls import dashboard_urlpatterns
from reviews.urls import reviews_urlpatterns
from actions.urls import actions_urlpatterns
from programs.urls import programs_urlpatterns
from applications.urls import applications_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(r"", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
]

urlpatterns += (accounts_urlpatterns
                + profile_urlpatterns
                + programs_urlpatterns
                + applications_urlpatterns
                + dashboard_urlpatterns
                + actions_urlpatterns
                + reviews_urlpatterns
                )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
