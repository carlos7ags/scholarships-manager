from datetime import datetime
from profile.models import *

from crispy_forms.bootstrap import Field, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.forms import ModelForm


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field("name"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("lastname_first", css_class="form-group col-md-4 mb-1"),
                Column("lastname_second", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("birthday", css_class="form-group col-md-4 mb-1"),
                Column("birth_place", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("nationality", css_class="form-group col-md-4 mb-1"),
                Column("curp", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("ine", css_class="form-group col-md-4 mb-1"),
                Column("passport", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("marital_status", css_class="form-group col-md-3 mb-1"),
                Column("gender", css_class="form-group col-md-2 mb-1"),
                Column("occupation", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("profile_picture"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = Profile
        exclude = ("validated",)
        widgets = {
            "birthday": forms.SelectDateWidget(
                years=range(datetime.now().year, 1900, -1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
        }


class ProfileAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                "<p>Deberas proporcionar una dirección valida en el Estado de Aguascalientes.</p>"
            ),
            Row(
                Column("street", css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("exterior_number", css_class="form-group col-md-2 mb-1"),
                Column("interior_number", css_class="form-group col-md-2 mb-1"),
                Column("suburb", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("postal_code", css_class="form-group col-md-3 mb-1"),
                Column("locality", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("municipality", css_class="form-group col-md-3 mb-1"),
                Column("state", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = Address
        exclude = ("validated",)


class ProfileContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("phone", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("mobile", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("email", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = Contact
        exclude = ("validated",)


class ProfileBankForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("bank_name", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("account_number", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("clabe", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = Bank
        exclude = ("validated",)


class ProfileEmergencyContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("address", css_class="form-group col-md-6 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("location", css_class="form-group col-md-3 mb-1"),
                Column("email", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("phone", css_class="form-group col-md-3 mb-1"),
                Column("mobile", css_class="form-group col-md-3 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = EmergencyContact
        exclude = ("validated",)
