from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, RedirectView

from .forms import *
from .models import *
import time


def create_application(request, id):
    if not Application.objects.filter(username=request.user, program=id).exists():
        if request.method == "POST":
            form = ApplicationForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.username = request.user
                obj.program = Program.objects.filter(id=id).first()
                prefix = obj.program.application_prefix
                folio = prefix + str(int(time.time()*10000))[3:]
                while Application.objects.filter(folio=folio).exists():
                    folio = prefix + str(int(time.time()*1000))[3:]
                obj.folio = folio
                obj.save()
    return redirect(reverse("home"))
