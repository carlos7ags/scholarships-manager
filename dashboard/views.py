from django.views.generic import TemplateView
from applications.models import Application
from django.db.models import Q


class StaffDashboardView(TemplateView):
    template_name = "staff_dashboard.html"


class ApplicantDashboardView(TemplateView):
    template_name = "applicant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_applications"] = Application.objects.filter(username=self.request.user, current_stage=0).all()
        context["sent_applications"] = Application.objects.filter(username=self.request.user).exclude(current_stage=0).all()
        return context
