from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, RedirectView

from .forms import *
from .models import *


class ExtendedUserCreateView(CreateView):

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = self.request.user
            obj.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


class ProfileCreate(ExtendedUserCreateView):
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("applicant-dashboard")


class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("applicant-dashboard")

    def request_user_is_owner(self, request):
        obj = self.get_object()
        return obj.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)


class ProfileRedirectView(RedirectView):
    def get_redirect_url(self):
        if Profile.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "profile-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("profile-create")


class ProfileAddressCreate(ExtendedUserCreateView):
    form_class = ProfileAddressForm
    template_name = "profile_address.html"
    success_url = reverse_lazy("applicant-dashboard")


class ProfileAddressUpdate(UpdateView):
    model = Address
    form_class = ProfileAddressForm
    template_name = "profile_address.html"
    success_url = reverse_lazy("applicant-dashboard")

    def request_user_is_owner(self, request):
        obj = self.get_object()
        return obj.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        return super(ProfileAddressUpdate, self).dispatch(request, *args, **kwargs)


class ProfileAddressRedirectView(RedirectView):
    def get_redirect_url(self):
        if Address.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "profile-address-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("profile-address-create")


class ProfileContactCreate(ExtendedUserCreateView):
    form_class = ProfileContactForm
    template_name = "profile_contact.html"
    success_url = reverse_lazy("applicant-dashboard")


class ProfileContactUpdate(UpdateView):
    model = Contact
    form_class = ProfileContactForm
    template_name = "profile_contact.html"
    success_url = reverse_lazy("applicant-dashboard")

    def request_user_is_owner(self, request):
        obj = self.get_object()
        return obj.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        return super(ProfileContactUpdate, self).dispatch(request, *args, **kwargs)


class ProfileContactRedirectView(RedirectView):
    def get_redirect_url(self):
        if Contact.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "profile-contact-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("profile-contact-create")


class ProfileBankCreate(ExtendedUserCreateView):
    form_class = ProfileBankForm
    template_name = "profile_bank.html"
    success_url = reverse_lazy("applicant-dashboard")


class ProfileBankUpdate(UpdateView):
    model = Bank
    form_class = ProfileBankForm
    template_name = "profile_bank.html"
    success_url = reverse_lazy("applicant-dashboard")

    def request_user_is_owner(self, request):
        obj = self.get_object()
        return obj.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        return super(ProfileBankUpdate, self).dispatch(request, *args, **kwargs)


class ProfileBankRedirectView(RedirectView):
    def get_redirect_url(self):
        if Bank.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "profile-bank-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("profile-bank-create")


class ProfileEmergencyContactCreate(ExtendedUserCreateView):
    form_class = ProfileEmergencyContactForm
    template_name = "profile_emergency_contact.html"
    success_url = reverse_lazy("applicant-dashboard")


class ProfileEmergencyContactUpdate(UpdateView):
    model = EmergencyContact
    form_class = ProfileEmergencyContactForm
    template_name = "profile_emergency_contact.html"
    success_url = reverse_lazy("applicant-dashboard")

    def request_user_is_owner(self, request):
        obj = self.get_object()
        return obj.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        return super(ProfileEmergencyContactUpdate, self).dispatch(request, *args, **kwargs)


class ProfileEmergencyContactRedirectView(RedirectView):
    def get_redirect_url(self):
        if EmergencyContact.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "profile-emergency-contact-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("profile-emergency-contact-create")
