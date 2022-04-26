from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, RedirectView, TemplateView
from actions.models import PendingTasks

from .forms import *
from .models import *


def complete_profile_task(http_referer: str, username: str):
    valid_form_types = ["personal", "address", "contact", "bank", "emergency"]
    pending_tasks = PendingTasks.objects.filter(username=username, completed=False)
    for task in pending_tasks:
        form_type = task.task.redirect_url.split("/")[1]
        if form_type in valid_form_types and form_type in http_referer:
            task.completed = True
            task.save()


def prettyfy_bank(bank: Bank):
    bank.clabe = ' '.join([bank.clabe[i:i+4] for i in range(0, len(bank.clabe), 4)])
    bank.account_number = ' '.join([bank.account_number[i:i+4] for i in range(0, len(bank.account_number), 4)])
    return bank


def prettyfy_emergency_contact(emergency: EmergencyContact):
    emergency.phone = f"({emergency.phone[:3]}) {emergency.phone[3:6]} {emergency.phone[6:]}"
    emergency.mobile = f"({emergency.mobile[:3]}) {emergency.mobile[3:6]} {emergency.mobile[6:]}"
    return emergency


def prettyfy_contact(contact: Contact):
    contact.phone = f"({contact.phone[:3]}) {contact.phone[3:6]} {contact.phone[6:]}"
    contact.mobile = f"({contact.mobile[:3]}) {contact.mobile[3:6]} {contact.mobile[6:]}"
    return contact


class ExtendedUserCreateView(CreateView):

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = self.request.user
            obj.save()
            complete_profile_task(request.META.get('HTTP_REFERER'), self.request.user)
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


class ExtendedUserUpdateView(UpdateView):

    def request_user_is_owner(self, request):
        obj = self.get_object()
        return obj.username == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.request_user_is_owner(request):
            return redirect_to_login(request.get_full_path())
        return super(ExtendedUserUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        complete_profile_task(request.META.get('HTTP_REFERER'), self.request.user)
        return super().post(request, *args, **kwargs)


class ProfileCreate(ExtendedUserCreateView):
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile-detail")


class ProfileUpdate(ExtendedUserUpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile-detail")


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
    success_url = reverse_lazy("profile-detail")


class ProfileAddressUpdate(ExtendedUserUpdateView):
    model = Address
    form_class = ProfileAddressForm
    template_name = "profile_address.html"
    success_url = reverse_lazy("profile-detail")


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
    success_url = reverse_lazy("profile-detail")


class ProfileContactUpdate(ExtendedUserUpdateView):
    model = Contact
    form_class = ProfileContactForm
    template_name = "profile_contact.html"
    success_url = reverse_lazy("profile-detail")


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
    success_url = reverse_lazy("profile-detail")


class ProfileBankUpdate(ExtendedUserUpdateView):
    model = Bank
    form_class = ProfileBankForm
    template_name = "profile_bank.html"
    success_url = reverse_lazy("profile-detail")


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
    success_url = reverse_lazy("profile-detail")


class ProfileEmergencyContactUpdate(ExtendedUserUpdateView):
    model = EmergencyContact
    form_class = ProfileEmergencyContactForm
    template_name = "profile_emergency_contact.html"
    success_url = reverse_lazy("profile-detail")


class ProfileEmergencyContactRedirectView(RedirectView):
    def get_redirect_url(self):
        if EmergencyContact.objects.filter(username=self.request.user.id).exists():
            return reverse(
                "profile-emergency-contact-update", kwargs={"pk": self.request.user.id}
            )
        else:
            return reverse("profile-emergency-contact-create")


class ProfileDetail(TemplateView):
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user
        context["profile"] = Profile.objects.filter(
            username=username
        ).first()
        context["bank"] = Bank.objects.filter(
            username=username
        ).first()
        if context["bank"]:
            context["bank"] = prettyfy_bank(context["bank"])
        context["address"] = Address.objects.filter(
            username=username
        ).first()

        context["contact"] = Contact.objects.filter(
            username=username
        ).first()
        if context["contact"]:
            context["contact"] = prettyfy_contact(context["contact"])

        context["emergency"] = EmergencyContact.objects.filter(
            username=username
        ).first()
        if context["emergency"]:
            context["emergency"] = prettyfy_emergency_contact(context["emergency"])

        return context
