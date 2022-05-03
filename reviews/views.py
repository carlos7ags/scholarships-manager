from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
)
from django_filters.views import FilterView

from applications.models import Application
from reviews.filters import ApplicationsFilter


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class ApplicationsListView(AdminStaffRequiredMixin, FilterView):
    model = Application
    queryset = Application.objects.filter().all()
    context_object_name = "staff_applications_list"
    template_name = "applications_list.html"
    filterset_class = ApplicationsFilter
    paginate_by = 25
    ordering = [
        "username",
        "-current_stage",
    ]
