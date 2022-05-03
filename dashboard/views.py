from django.views.generic import TemplateView
from applications.models import Application
from actions.models import PendingTasks
from reviews.views import AdminStaffRequiredMixin


class StaffDashboardView(AdminStaffRequiredMixin, TemplateView):
    template_name = "staff_dashboard.html"


class ApplicantDashboardView(TemplateView):
    template_name = "applicant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applications"] = Application.objects.filter(username=self.request.user).order_by("-current_stage").all()
        context["actions"] = PendingTasks.objects.filter(username=self.request.user, completed=False).order_by("deadline").all()
        return context
