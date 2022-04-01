from django.contrib.auth.decorators import login_required
from django.urls import path

from profile.views import *

profile_urlpatterns = [
    path("profile",
         login_required(ProfileDetail.as_view()),
         name="profile-detail"
         ),

    path("profile/personal",
         login_required(ProfileCreate.as_view()),
         name="profile-create"
         ),
    path(
        "profile/<pk>/personal/update",
        login_required(ProfileUpdate.as_view()),
        name="profile-update",
        ),
    path(
        "profile/personal/redirect",
        login_required(ProfileRedirectView.as_view()),
        name="profile-redirect",
        ),

    path("profile/address",
         login_required(ProfileAddressCreate.as_view()),
         name="profile-address-create"
         ),
    path(
        "profile/<pk>/address/update",
        login_required(ProfileAddressUpdate.as_view()),
        name="profile-address-update",
        ),
    path(
        "profile/address/redirect",
        login_required(ProfileAddressRedirectView.as_view()),
        name="profile-address-redirect",
        ),

    path("profile/contact",
         login_required(ProfileContactCreate.as_view()),
         name="profile-contact-create"
         ),
    path(
        "profile/<pk>/contact/update",
        login_required(ProfileContactUpdate.as_view()),
        name="profile-contact-update",
    ),
    path(
        "profile/contact/redirect",
        login_required(ProfileContactRedirectView.as_view()),
        name="profile-contact-redirect",
        ),

    path("profile/bank",
         login_required(ProfileBankCreate.as_view()),
         name="profile-bank-create"
         ),
    path(
        "profile/<pk>/bank/update",
        login_required(ProfileBankUpdate.as_view()),
        name="profile-bank-update",
        ),
    path(
        "profile/bank/redirect",
        login_required(ProfileBankRedirectView.as_view()),
        name="profile-bank-redirect",
        ),

    path("profile/emergencycontact",
         login_required(ProfileEmergencyContactCreate.as_view()),
         name="profile-emergency-contact-create"
         ),
    path(
        "profile/<pk>/emergencycontact/update",
        login_required(ProfileEmergencyContactUpdate.as_view()),
        name="profile-emergency-contact-update",
        ),
    path(
        "profile/emergencycontact/redirect",
        login_required(ProfileEmergencyContactRedirectView.as_view()),
        name="profile-emergency-contact-redirect",
        ),
]
