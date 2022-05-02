import os
from typing import Dict, Any

from django.contrib.auth.views import redirect_to_login
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, View

from profile.models import Profile
from .forms import *
from .models import *
import time
import json
from django.core.mail import send_mail
from django.template import loader
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


def send_application_sent_mail(curp: str, program_code: str, program_name: str):
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
        "contacto.fibeipes@gmail.com",
        ["cabrera1988reinier@gmail.com"],
        fail_silently=False,
        html_message=html_message,
    )


def create_application_form(request, pk):
    obj = Application.objects.filter(id=pk).first()
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        obj.application_form = data
        obj.current_stage = 1
        send_application_sent_mail(curp=request.user.username, program_code=obj.program.application_prefix, program_name=obj.program.title)
        obj.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    return HttpResponse('{"status":"fail"}', content_type='application/json')


def withdraw_application(request, pk):
    if request.method == "POST":
        obj = Application.objects.filter(id=pk).first()
        obj.current_stage = -1
        obj.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'refreshMain'})
    else:
        return render(request, 'withdraw_application.html')


def create_application(request, program_id):
    application = Application.objects.filter(username=request.user, program=program_id).first()
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
                folio = prefix + str(int(time.time()*10000))[3:]
                while Application.objects.filter(folio=folio).exists():
                    folio = prefix + str(int(time.time()*1000))[3:]
                obj.folio = folio
                obj.save()
                return redirect(reverse("render-application-form", args=(obj.id,)))
            else:
                raise Http404
        else:
            raise Http404


def download_application(request, pk):
    if request.method == "GET":
        context_dict = dict()
        context_dict["request"] = request
        context_dict["profile"] = Profile.objects.filter(username=request.user).first()
        context_dict["application"] = Application.objects.filter(id=pk).first()
        pdf = html_to_pdf("ad-solicitud-pdf.html", context=context_dict)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return Http404


class RenderApplicationFormView(TemplateView):
    template_name = "create_application_form.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = Application.objects.filter(id=self.kwargs["pk"]).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        context["application_form_template"] = self.object.program.application_form.template
        return context

    def request_user_is_owner(self, request):
        obj = self.object
        return obj.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        if self.object.application_form:
            return redirect(reverse("application-detail", args=(self.object.id,)))
        return super(RenderApplicationFormView, self).dispatch(request, *args, **kwargs)


class ApplicationDetailView(DetailView):
    model = Application
    template_name = "application_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_form = context["object"].application_form
        context["application"] = zip(
            [app_form[k]["label"] for k in app_form.keys()],
            [app_form[k]["value"] for k in app_form.keys()],
        )
        return context

    def get_queryset(self):
        return Application.objects.filter(username=self.request.user)


def html_to_pdf(template_src: str, context=Dict[str, Any]):
    template = get_template(template_src)
    html = template.render(context)
    print(html)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path