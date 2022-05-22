from profile.models import Address, Bank, Contact, EmergencyContact, Profile
from profile.views import (prettyfy_bank, prettyfy_contact,
                           prettyfy_emergency_contact)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django_filters.views import FilterView

from actions.models import PendingTasks
from applications.models import Application, ApplicationContentApoyo, ApplicationContentConvocatoria
from reviews.filters import ApplicationsFilter
from reviews.models import ReviewersProgramACL


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class ApplicationsListView(AdminStaffRequiredMixin, FilterView):
    model = Application
    context_object_name = "staff_applications_list"
    template_name = "applications_list.html"
    filterset_class = ApplicationsFilter
    paginate_by = 25
    ordering = [
        "username",
        "-current_stage",
    ]

    def get_queryset(self):
        acl_programs = ReviewersProgramACL.objects.filter(username=self.request.user).values_list("program", flat=True)
        return Application.objects.filter(program__in=acl_programs).all()


class ApplicationDetailReview(AdminStaffRequiredMixin, TemplateView):
    template_name = "application_detail_review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = Application.objects.filter(id=kwargs["pk"]).first()

        if application.program.application_form_type == "convocatoria":
            context["application"] = ApplicationContentConvocatoria.objects.filter(id=application).first()
        elif application.program.application_form_type == "apoyo":
            context["application"] = ApplicationContentApoyo.objects.filter(id=application).first()

        context["folio"] = application.folio
        context["application_id"] = kwargs["pk"]
        context["application_validated"] = application.validated

        username = application.username
        context["profile"] = Profile.objects.filter(username=username).first()
        context["bank"] = Bank.objects.filter(username=username).first()
        if context["bank"]:
            context["bank"] = prettyfy_bank(context["bank"])
        context["address"] = Address.objects.filter(username=username).first()

        context["contact"] = Contact.objects.filter(username=username).first()
        if context["contact"]:
            context["contact"] = prettyfy_contact(context["contact"])

        context["emergencycontact"] = EmergencyContact.objects.filter(
            username=username
        ).first()
        if context["emergencycontact"]:
            context["emergencycontact"] = prettyfy_emergency_contact(
                context["emergencycontact"]
            )

        return context


def validate_application(request, pk):
    if request.method == "POST":
        obj = Application.objects.filter(id=pk).first()
        obj.current_stage = 3
        obj.validated = True
        obj.save()
        return redirect(reverse("staff-applications-list"))


def comment_application(request, pk):
    if request.method == "POST":
        application = Application.objects.filter(id=pk).first()
        application.current_stage = 2
        application.save()
        """
        obj = PendingTasks()
        obj.username = application.username
        obj.comments = request.body.comments
        obj.save()
        """
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshMain"})
    else:
        return render(request, "comment_application.html")
