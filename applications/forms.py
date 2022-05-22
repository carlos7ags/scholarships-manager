from datetime import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Column, Field, Row, Layout
from django.forms import ModelForm
from applications.models import Application, ApplicationContentConvocatoria, ApplicationContentApoyo
from django import forms


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ()


class ApplicationConvocatoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("date_start", css_class="form-group col-md-4 mb-1"),
                Column("date_end", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("program_description"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = ApplicationContentConvocatoria
        exclude = ("validated",)
        widgets = {
            "date_start": forms.SelectDateWidget(
                years=range(datetime.now().year + 10, datetime.now().year - 5, -1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
            "date_end": forms.SelectDateWidget(
                years=range(datetime.now().year + 10, datetime.now().year - 5, -1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
        }


class ApplicationApoyoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("date_start", css_class="form-group col-md-4 mb-1"),
                Column("date_end", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("program_name"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = ApplicationContentApoyo
        exclude = ("validated",)
        widgets = {
            "date_start": forms.SelectDateWidget(
                years=range(datetime.now().year + 10, datetime.now().year - 5, -1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
            "date_end": forms.SelectDateWidget(
                years=range(datetime.now().year + 10, datetime.now().year - 5, -1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
        }
