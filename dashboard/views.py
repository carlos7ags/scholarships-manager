from django.views.generic import TemplateView

from actions.models import PendingTasks
from applications.models import Application, Award
from reviews.views import AdminStaffRequiredMixin


class StaffDashboardView(AdminStaffRequiredMixin, TemplateView):
    template_name = "staff_dashboard.html"


class ApplicantDashboardView(TemplateView):
    template_name = "applicant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = (
            Application.objects.filter(username=self.request.user)
            .order_by("-current_stage")
            .all()
        )
        decisions = [Award.objects.filter(id=application).first() for application in applications]
        context["applications"] = list(zip(applications, decisions))
        context["actions"] = (
            PendingTasks.objects.filter(username=self.request.user, completed=False)
            .order_by("deadline")
            .all()
        )
        return context
