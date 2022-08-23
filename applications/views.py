import io
import time
from datetime import date

from django.contrib.humanize.templatetags import humanize
from django.contrib.staticfiles.finders import find
from django.core.exceptions import ValidationError
from django.templatetags.static import static
from babel.dates import format_date

from profile.models import Profile, EmergencyContact, Bank, Address, Contact
from typing import Dict

from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, RedirectView, UpdateView

from actions.models import PendingTasks

from .forms import ApplicationApoyoForm, ApplicationConvocatoriaForm, ApplicationForm, AwardDeliverableForm
from .models import *

from docxtpl import DocxTemplate


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
        context_dict["contact"] = Contact.objects.filter(username=request.user).first()
        context_dict["emergency_contact"] = EmergencyContact.objects.filter(username=request.user).first()
        context_dict["bank"] = Bank.objects.filter(username=request.user).first()
        context_dict["address"] = Address.objects.filter(username=request.user).first()
        context_dict["application_base"] = Application.objects.filter(id=pk).first()
        if context_dict["application_base"].program.application_form_type == "convocatoria":
            context_dict["application"] = ApplicationContentConvocatoria.objects.filter(id=pk).first()
            doc = docx_template_generator_convocatoria(context_dict)
        else:
            context_dict["application"] = ApplicationContentApoyo.objects.filter(id=pk).first()
            doc = docx_template_generator_apoyo(context_dict)
        response = HttpResponse(doc, content_type="application/application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response["Content-Disposition"] = 'attachment; filename = "solicitud.docx"'
        response["Content-Encoding"] = "UTF-8"
        return response
    else:
        return Http404


def upload_final_proof(request, pk):
    award = Award.objects.get(id=pk)
    if request.method == "POST":
        if not request.FILES:
            raise ValidationError('No se adjunto el documento.')
        print(request.FILES)
        form = AwardDeliverableForm(request.POST, request.FILES, instance=award)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "refreshMain"})
    else:
        form = AwardDeliverableForm(instance=award)
        return render(request, "upload_final_proof.html", {'form': form})


def non_null(text):
    text = str(text) if text else ""
    return text


def prettify(text):
    text = str(text) if text else ""
    text = text.title()
    return text


def prettify_phone(text):
    text = prettify(text)
    if text:
        text = f"{text[:3]}-{text[3:6]}-{text[6:]}"
    return text


def docx_template_generator_convocatoria(data: Dict):
    path = find("docs/plantilla_solicitud.docx")
    doc = DocxTemplate(path)
    context = dict()

    context['curp'] = data["request"].user.username.upper()

    profile = data["profile"]
    full_name = f"{prettify(profile.lastname_first)} {prettify(profile.lastname_second)} {prettify(profile.name)}"
    context['full_name'] = full_name.replace("  ", " ")
    context['birthday'] = format_date(profile.birthday, format='long', locale='es')
    context['nationality'] = prettify(profile.nationality)
    context['birth_place'] = prettify(profile.get_birth_place_display())
    context['age'] = prettify(int((date.today() - profile.birthday).days / 365.2425))
    context['gender'] = prettify(profile.get_gender_display())
    context['marital_status'] = prettify(profile.get_marital_status_display())
    context['passport'] = prettify(profile.passport).upper()
    context['ine'] = prettify(profile.ine)
    context['occupation'] = prettify(profile.occupation)

    address = data["address"]
    context['street'] = prettify(address.street)
    context['exterior_number'] = prettify(address.exterior_number)
    context['interior_number'] = prettify(address.interior_number)
    context['postal_code'] = prettify(address.postal_code)
    context['municipality'] = prettify(address.municipality)
    context['locality'] = prettify(address.locality)
    context['suburb'] = prettify(address.suburb)
    context['state'] = prettify(address.get_state_display())

    contact = data["contact"]
    context['phone'] = prettify_phone(contact.phone)
    context['mobile'] = prettify_phone(contact.mobile)
    context['email'] = prettify(data["request"].user.email).lower()

    bank = data["bank"]
    context['bank_name'] = prettify(bank.bank_name)
    context['account_number'] = prettify(bank.account_number)
    context['clabe'] = prettify(bank.clabe)

    emergency_contact = data["emergency_contact"]
    context["emergency_contact_name"] = prettify(emergency_contact.name)
    context["emergency_contact_relationship"] = prettify(emergency_contact.relationship)
    context["emergency_contact_phone"] = prettify_phone(emergency_contact.phone)
    context["emergency_contact_mobile"] = prettify_phone(emergency_contact.mobile)
    context["emergency_contact_email"] = prettify(emergency_contact.email).lower()
    context["emergency_contact_country"] = prettify(emergency_contact.country)
    context["emergency_contact_city"] = prettify(emergency_contact.city)

    application = data["application"]
    application_base = data["application_base"]
    context["application_id"] = prettify(application_base.id)
    context["application_folio"] = prettify(application_base.folio).upper()
    context["application_updated_at"] = format_date(application.updated_at, format='long', locale='es')
    context["application_date_start"] = format_date(application.date_start, format='long', locale='es')
    context["application_date_end"] = format_date(application.date_end, format='long', locale='es')
    context["application_program_name"] = prettify(application.program_name)
    context["application_objective"] = prettify(application.objective).capitalize()
    context["application_area"] = prettify(application.area)
    context["application_research_topic"] = non_null(application.research_topic)
    context["application_location"] = prettify(application.location)
    context["application_institution"] = prettify(application.institution)
    context["application_duration_hours"] = prettify(application.duration_hours)

    context["application_personal_statement"] = prettify(application.personal_statement)
    context["application_suitability"] = prettify(application.suitability)
    context["application_future_plans"] = prettify(application.future_plans)
    context["application_importance"] = prettify(application.importance)

    context["application_total_movilidad"] = humanize.intcomma(application.total_movilidad)
    context["application_requested_movilidad"] = humanize.intcomma(application.requested_movilidad)
    context["application_total_investigacion"] = humanize.intcomma(application.total_investigacion)
    context["application_requested_investigacion"] = humanize.intcomma(application.requested_investigacion)
    context["application_total_inscripcion"] = humanize.intcomma(application.total_inscripcion)
    context["application_requested_inscripcion"] = humanize.intcomma(application.requested_inscripcion)
    context["application_total_viaticos"] = humanize.intcomma(application.total_viaticos)
    context["application_requested_viaticos"] = humanize.intcomma(application.requested_viaticos)
    context["application_total_otros"] = humanize.intcomma(application.total_otros)
    context["application_requested_otros"] = humanize.intcomma(application.requested_otros)

    context["application_project_name"] = prettify(application.project_name)
    context["application_objective"] = prettify(application.objective).capitalize()
    context["application_program_relation_cti"] = prettify(application.program_relation_cti).capitalize()
    context["application_program_relation_state"] = prettify(application.program_relation_state).capitalize()
    context["application_description"] = prettify(application.description).capitalize()
    context["application_impact"] = prettify(application.impact).capitalize()
    context["application_statement_of_purpose"] = non_null(application.statement_of_purpose)
    context["application_credits"] = non_null(application.credits)
    context["application_language"] = non_null(application.language)

    context["application_current_job"] = non_null(application.current_job)
    context["application_last_academic_grade"] = non_null(application.last_academic_grade)
    context["application_last_grade"] = non_null(application.last_grade)

    doc.render(context)

    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()


def docx_template_generator_apoyo(data: Dict):
    path = find("docs/plantilla_solicitud.docx")
    doc = DocxTemplate(path)
    context = dict()

    context['curp'] = data["request"].user.username.upper()

    profile = data["profile"]
    full_name = f"{prettify(profile.lastname_first)} {prettify(profile.lastname_second)} {prettify(profile.name)}"
    context['full_name'] = full_name.replace("  ", " ")
    context['nationality'] = prettify(profile.nationality)
    context['birth_place'] = prettify(profile.get_birth_place_display())
    context['age'] = prettify(int((date.today() - profile.birthday).days / 365.2425))
    context['gender'] = prettify(profile.get_gender_display())
    context['marital_status'] = prettify(profile.get_marital_status_display())
    context['passport'] = prettify(profile.passport).upper()
    context['ine'] = prettify(profile.ine)
    context['occupation'] = prettify(profile.occupation)

    address = data["address"]
    context['street'] = prettify(address.street)
    context['exterior_number'] = prettify(address.exterior_number)
    context['interior_number'] = prettify(address.interior_number)
    context['postal_code'] = prettify(address.postal_code)
    context['municipality'] = prettify(address.municipality)
    context['locality'] = prettify(address.locality)
    context['suburb'] = prettify(address.suburb)
    context['state'] = prettify(address.get_state_display())

    contact = data["contact"]
    context['phone'] = prettify_phone(contact.phone)
    context['mobile'] = prettify_phone(contact.mobile)
    context['email'] = prettify(data["request"].user.email).lower()

    bank = data["bank"]
    context['bank_name'] = prettify(bank.bank_name)
    context['account_number'] = prettify(bank.account_number)
    context['clabe'] = prettify(bank.clabe)

    emergency_contact = data["emergency_contact"]
    context["emergency_contact_name"] = prettify(emergency_contact.name)
    context["emergency_contact_relationship"] = prettify(emergency_contact.relationship)
    context["emergency_contact_phone"] = prettify_phone(emergency_contact.phone)
    context["emergency_contact_mobile"] = prettify_phone(emergency_contact.mobile)
    context["emergency_contact_email"] = prettify(emergency_contact.email).lower()
    context["emergency_contact_country"] = prettify(emergency_contact.country)
    context["emergency_contact_city"] = prettify(emergency_contact.city)

    doc.render(context)


    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()
