from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail

from profile.models import Address, Bank, Contact, EmergencyContact, Profile
from profile.views import (prettyfy_bank, prettyfy_contact,
                           prettyfy_emergency_contact)
from django.template import loader

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django_filters.views import FilterView

from actions.models import PendingTasks, Task
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
        context["application_stage"] = application.current_stage

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
        redirect_url = "application/<application_id>/task/<task_id>/update"
        application = Application.objects.filter(id=pk).first()
        application.current_stage = 2
        send_observations_mail(username=application.username, request=request, application=application)
        application.save()
        task = Task.objects.filter(redirect_url=redirect_url).first()
        if task:
            new_task = PendingTasks()
            new_task.task = task
            new_task.username = application.username
            new_task.comments = request.POST["comment"]
            new_task.save()
            new_task.redirect_url_overwrite = redirect_url.replace("<application_id>", pk).replace("<task_id>", str(new_task.id))
            new_task.save()
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshMain"})
    else:
        return render(request, "comment_application.html")


def send_observations_mail(username: User, request: HttpRequest, application: Application):
    html_message = loader.render_to_string(
        "comments_mail.html",
        {
            "folio": application.folio,
            "curp": username.username,
            "program": application.program.title,
            "code": application.program.application_prefix,
            "comments": request.body,
        },
    )
    send_mail(
        f"Fomento a Talentos - Observaciones a solicitud - {application.folio}",
        "",
        "apoyoatalentos@gmail.com",
        [username.email],
        fail_silently=True,
        html_message=html_message,
    )
