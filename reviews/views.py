from datetime import datetime, timedelta
from profile.models import Address, Bank, Contact, EmergencyContact, Profile
from profile.views import (prettyfy_bank, prettyfy_contact,
                           prettyfy_emergency_contact)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.views.generic import (CreateView, RedirectView, TemplateView,
                                  UpdateView)
from django_filters.views import FilterView

from actions.models import PendingTasks, Task
from applications.models import (Application, ApplicationContentApoyo,
                                 ApplicationContentConvocatoria, Award)
from programs.models import Program
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
        acl_programs = ReviewersProgramACL.objects.filter(
            username=self.request.user
        ).values_list("program", flat=True)
        return Application.objects.filter(program__in=acl_programs).all()


class ApplicationDetailReview(AdminStaffRequiredMixin, TemplateView):
    template_name = "application_detail_review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = Application.objects.filter(id=kwargs["pk"]).first()

        if application.program.application_form_type == "convocatoria":
            context["application"] = ApplicationContentConvocatoria.objects.filter(
                id=application
            ).first()
        elif application.program.application_form_type == "apoyo":
            context["application"] = ApplicationContentApoyo.objects.filter(
                id=application
            ).first()

        context["folio"] = application.folio
        context["program_id"] = application.program.id
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


def receive_application_documents(request, pk):
    if request.method == "POST":
        action_key = "documentacion"
        application = Application.objects.filter(id=pk).first()
        task = Task.objects.filter(redirect_url=action_key).first()
        obj = PendingTasks.objects.filter(application=application, task=task).first()
        obj.completed = True
        obj.save()
        return redirect(reverse("staff-applications-list"))


def validate_application(request, pk):
    if request.method == "POST":
        action_key = "documentacion"
        application = Application.objects.filter(id=pk).first()
        application.current_stage = 3
        application.validated = True
        application.save()
        task = Task.objects.filter(redirect_url=action_key).first()
        if task:
            new_task = PendingTasks()
            new_task.task = task
            new_task.username = application.username
            new_task.application = application
            if task.has_deadline:
                new_task.deadline = datetime.now() + timedelta(
                    days=task.days_to_complete
                )
            new_task.save()
        return redirect(reverse("staff-applications-list"))


def comment_application(request, pk):
    if request.method == "POST":
        redirect_url = "application/<application_id>/task/<task_id>/update"
        application = Application.objects.filter(id=pk).first()
        application.current_stage = 2
        send_observations_mail(
            username=application.username, request=request, application=application
        )
        application.save()
        task = Task.objects.filter(redirect_url=redirect_url).first()
        if task:
            new_task = PendingTasks()
            new_task.task = task
            new_task.username = application.username
            new_task.application = application
            new_task.comments = request.POST["comment"]
            new_task.save()
            new_task.redirect_url_overwrite = redirect_url.replace(
                "<application_id>", pk
            ).replace("<task_id>", str(new_task.id))
            new_task.save()
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshMain"})
    else:
        return render(request, "comment_application.html")


def send_observations_mail(
    username: User, request: HttpRequest, application: Application
):
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


# ToDo: luego falta cargar el archivo final comprobante y la descarga de la solicitud


class ApplicationAwardCreate(CreateView):
    model = Award
    template_name = "application_award.html"

    def get_success_url(self):
        return HttpResponseRedirect(self.request.META.get("HTTP_REFERER"))


class ApplicationAwardUpdate(UpdateView):
    model = Award
    template_name = "application_award.html"

    def get_success_url(self):
        return HttpResponseRedirect(self.request.META.get("HTTP_REFERER"))


class ApplicationAwardRedirect(RedirectView):
    def get_redirect_url(self, program_id, application_id):
        program = Program.objects.filter(id=program_id).fisrst()
        award = Award.objects.filter(
            username=self.request.user.id, program=program
        ).first()
        if award:
            return reverse(
                "staff-application-award-update",
                kwargs={
                    "program_id": program_id,
                    "application_id": application_id,
                    "pk": award.id,
                },
            )
        else:
            return reverse(
                "staff-application-award-create",
                kwargs={
                    "program_id": program_id,
                    "application_id": application_id,
                },
            )
