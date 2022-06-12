from datetime import datetime

from applications.models import Award
from profile.models import *

from crispy_forms.bootstrap import Field, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.forms import ModelForm


class AwardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field("decision"), css_class="form-group col-md-4 mb-1"),
                Column(Field("awarded"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("comments"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("acta"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("require_deliverable", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column("deliverable_by", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = Award
        exclude = ("id", "username", "program", "validated", "deliverable", "deliverable_validated", "created_at", "updated_at")
        widgets = {
            "deliverable_by": forms.SelectDateWidget(
                years=range(datetime.now().year, datetime.now().year + 10, 1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
        }
