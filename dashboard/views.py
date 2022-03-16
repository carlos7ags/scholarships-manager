from django.views.generic import TemplateView
from applications.models import Application


class StaffDashboardView(TemplateView):
    template_name = "staff_dashboard.html"


class ApplicantDashboardView(TemplateView):
    template_name = "applicant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applications"] = Application.objects.filter(username=self.request.user).order_by("-current_stage").all()
        return context
