from datetime import date

from django.views.generic import TemplateView
from .models import *
from profile.models import *


class ProgramsListView(TemplateView):
    template_name = "programs_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programs = Program.objects.all().filter(publicity=True).order_by("-no_close_date", "-end_date")
        status = [
            ((program.start_date <= date.today() <= (program.end_date or date.today())) or program.no_close_date)
            for program in programs
        ]
        registered = [False for _ in programs]
        context["programs"] = zip(programs, status, registered)
        # context["completed_basic_forms"] = self.check_complete_forms()
        context["completed_basic_forms"] = True
        return context

    def check_complete_forms(self):
        profile = Profile.objects.filter(username=self.request.user.id).exists()
        address = Address.objects.filter(username=self.request.user.id).exists()
        contact = Contact.objects.filter(username=self.request.user.id).exists()
        emergency_contact = EmergencyContact.objects.filter(username=self.request.user.id).exists()
        bank = Bank.objects.filter(username=self.request.user.id).exists()
        return all([profile, address, contact, bank, emergency_contact])
