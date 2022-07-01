import os
import time
from io import BytesIO
from profile.models import Profile
from typing import Any, Dict

from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, RedirectView, UpdateView
from xhtml2pdf import pisa

from actions.models import PendingTasks

from .forms import ApplicationApoyoForm, ApplicationConvocatoriaForm, ApplicationForm
from .models import *


def send_application_sent_mail(
    to: str, curp: str, program_code: str, program_name: str
):
    try:
        html_message = loader.render_to_string(
            "application_sent_mail.html",
            {
                "curp": curp,
                "convocatoria": program_name,
                "codigo": program_code,
            },
        )
        send_mail(
            f"Fomento a Talentos - Nueva solicitud - {curp}",
            "",
            "apoyoatalentos@gmail.com",
            [to],
            fail_silently=False,
            html_message=html_message,
        )
    except OSError:
        pass


def withdraw_application(request, pk):
    if request.method == "POST":
        obj = Application.objects.filter(id=pk).first()
        obj.current_stage = -1
        obj.save()
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshMain"})
    else:
        return render(request, "withdraw_application.html")


def update_application(request, application_id, task_id):
    if request.method == "POST":
        application = Application.objects.filter(id=application_id).first()
        application.current_stage = 1
        task = PendingTasks.objects.filter(id=task_id).first()
        task.completed = True
        application.save()
        task.save()
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshMain"})
    else:
        task = PendingTasks.objects.filter(id=task_id).first()
        return render(request, "update_application.html", {"comments": task.comments})


def create_application(request, program_id):
    application = Application.objects.filter(
        username=request.user, program=program_id
    ).first()
    if application:
        return redirect(reverse("applicant-dashboard"))
    else:
        if request.method == "POST":
            form = ApplicationForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.username = request.user
                obj.program = Program.objects.filter(id=program_id).first()
                prefix = obj.program.application_prefix
                folio = prefix + str(int(time.time() * 10000))[3:]
                while Application.objects.filter(folio=folio).exists():
                    folio = prefix + str(int(time.time() * 1000))[3:]
                obj.folio = folio
                obj.save()
                return redirect(
                    reverse(
                        "application-form-redirect",
                        kwargs={"application_id": obj.id, "program_id": program_id},
                    )
                )
            else:
                raise Http404
        else:
            raise Http404


def complete_application_task(username: User, application_id: str):
    pending_tasks = PendingTasks.objects.filter(username=username, completed=False)
    for task in pending_tasks:
        if isinstance(task.redirect_url_overwrite, str):
            path_parts = task.task.redirect_url.split("/")
            form_type = path_parts[2]
            task_application_id = path_parts[3]
            if (
                "application" in form_type
                and str(application_id) == task_application_id
            ):
                task.completed = True
                task.save()


class ExtendedFormCreateView(CreateView):
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            application = Application.objects.filter(id=self.kwargs["pk"]).first()
            obj.id = application
            obj.save()
            application.current_stage = 1
            application.save()
            send_application_sent_mail(
                to="fomentoatalentos@gmail.com",
                curp=application.username,
                program_code=application.program.application_prefix,
                program_name=application.program.title,
            )
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


class ExtendedFormUpdateView(UpdateView):
    def request_user_is_owner(self, request):
        obj = self.get_object()
        return obj.id.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        return super(ExtendedFormUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        complete_application_task(
            username=self.request.user, application_id=self.kwargs["pk"]
        )
        return super().post(request, *args, **kwargs)


class ApplicationFormConvocatoriaCreate(ExtendedFormCreateView):
    form_class = ApplicationConvocatoriaForm
    template_name = "application_form.html"
    success_url = reverse_lazy("applicant-dashboard")


class ApplicationFormConvocatoriaUpdate(ExtendedFormUpdateView):
    model = ApplicationContentConvocatoria
    form_class = ApplicationConvocatoriaForm
    template_name = "application_form.html"
    success_url = reverse_lazy("applicant-dashboard")


class ApplicationFormApoyoCreate(ExtendedFormCreateView):
    form_class = ApplicationApoyoForm
    template_name = "application_form.html"
    success_url = reverse_lazy("applicant-dashboard")


class ApplicationFormApoyoUpdate(ExtendedFormUpdateView):
    model = ApplicationContentApoyo
    form_class = ApplicationApoyoForm
    template_name = "application_form.html"
    success_url = reverse_lazy("applicant-dashboard")


class ApplicationFormRedirect(RedirectView):
    def get_redirect_url(self, program_id, application_id):
        program = Program.objects.filter(id=program_id).first()
        if program.application_form_type == "convocatoria":
            if ApplicationContentConvocatoria.objects.filter(
                id=application_id
            ).exists():
                return reverse(
                    "application-form-convocatoria-update",
                    kwargs={"pk": application_id},
                )
            else:
                return reverse(
                    "application-form-convocatoria-create",
                    kwargs={"pk": application_id},
                )
        elif program.application_form_type == "apoyo":
            if ApplicationContentApoyo.objects.filter(id=application_id).exists():
                return reverse(
                    "application-form-apoyo-update", kwargs={"pk": application_id}
                )
            else:
                return reverse(
                    "application-form-apoyo-create", kwargs={"pk": application_id}
                )


def download_application(request, pk):
    if request.method == "GET":
        context_dict = dict()
        context_dict["request"] = request
        context_dict["profile"] = Profile.objects.filter(username=request.user).first()
        context_dict["application"] = Application.objects.filter(id=pk).first()
        pdf = html_to_pdf("ad-solicitud-pdf.html", context=context_dict)
        return HttpResponse(pdf, content_type="application/pdf")
    else:
        return Http404


def html_to_pdf(template_src: str, context=Dict[str, Any]):
    template = get_template(template_src)
    html = template.render(context)
    print(html)
    result = BytesIO()

    pdf = pisa.pisaDocument(
        BytesIO(html.encode("utf-8")), result, link_callback=fetch_resources
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path


def send_final_proof(request, pk):
    if request.method == "POST":
        application = Application.objects.filter(id=pk).first()
        # ToDo: agregar logica para subir archivo
        application.current_stage = 6
        application.save()
        return HttpResponse(status=204, headers={"HX-Trigger": "refreshMain"})
    else:
        return render(request, "send_final_proof.html")
