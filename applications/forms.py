import os
from datetime import datetime

from crispy_forms.bootstrap import FormActions, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row, Submit
from django import forms
from django.forms import ModelForm

from applications.models import (
    Application,
    ApplicationContentApoyo,
    ApplicationContentConvocatoria, Award,
)


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
                Column(
                    Field("program_description"), css_class="form-group col-md-8 mb-1"
                ),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = ApplicationContentConvocatoria
        exclude = ("validated", "id")
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
        self.fields["total_movilidad"].label = ""
        self.fields["requested_movilidad"].label = ""
        self.fields["total_investigacion"].label = ""
        self.fields["requested_investigacion"].label = ""
        self.fields["total_inscripcion"].label = ""
        self.fields["requested_inscripcion"].label = ""
        self.fields["total_viaticos"].label = ""
        self.fields["requested_viaticos"].label = ""
        self.fields["total_otros"].label = ""
        self.fields["requested_otros"].label = ""
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<h5>Información del programa de estudios</h5>"),
            Row(
                Column("date_start", css_class="form-group col-md-4 mb-1"),
                Column("date_end", css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("program_name"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("name"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("description"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("objective"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("credits"), css_class="form-group col-md-4 mb-1"),
            ),
            Row(
                Column(Field("duration_hours"), css_class="form-group col-md-4 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("language"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("area"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("impact"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("institution"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("location"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("materias"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("research_topic"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("program_requirements"), css_class="form-group col-md-8 mb-1"
                ),
                css_class="form-row",
            ),
            HTML("<h5>Apoyo solicitado</h5>"),
            HTML(
                "<p>El monto total del apoyo solicitado no puede exceder $20,000.00 al extranjero y $10,000.00 al interior del país.</p>"
            ),
            Div(
                HTML('<table class="table table-sm w-auto"'),
                HTML('<thead class="thead-dark">'),
                HTML("<tr>"),
                HTML('<th scope="col">Concepto de apoyo</th>'),
                HTML('<th scope="col">Monto solicitado</th>'),
                HTML('<th scope="col">Costo total</th>'),
                HTML("</tr>"),
                HTML("</thead>"),
                HTML("<tbody>"),
                HTML("<tr>"),
                HTML('<th scope="row">Movilidad</th>'),
                HTML("<td>"),
                PrependedText(
                    "total_movilidad", "$", css_class="form-group text-right col-md-6"
                ),
                HTML("</td>"),
                HTML("<td>"),
                PrependedText(
                    "requested_movilidad",
                    "$",
                    css_class="form-group text-right col-md-6",
                ),
                HTML("</td>"),
                HTML("</tr>"),
                HTML("<tr>"),
                HTML('<th scope="row">Investigación</th>'),
                HTML("<td>"),
                PrependedText(
                    "total_investigacion",
                    "$",
                    css_class="form-group text-right col-md-6",
                ),
                HTML("</td>"),
                HTML("<td>"),
                PrependedText(
                    "requested_investigacion",
                    "$",
                    css_class="form-group text-right col-md-6",
                ),
                HTML("</td>"),
                HTML("</tr>"),
                HTML("<tr>"),
                HTML('<th scope="row">Inscripción</th>'),
                HTML("<td>"),
                PrependedText(
                    "total_inscripcion", "$", css_class="form-group text-right col-md-6"
                ),
                HTML("</td>"),
                HTML("<td>"),
                PrependedText(
                    "requested_inscripcion",
                    "$",
                    css_class="form-group text-right col-md-6",
                ),
                HTML("</td>"),
                HTML("</tr>"),
                HTML("<tr>"),
                HTML('<th scope="row">Viáticos</th>'),
                HTML("<td>"),
                PrependedText(
                    "total_viaticos", "$", css_class="form-group text-right col-md-6"
                ),
                HTML("</td>"),
                HTML("<td>"),
                PrependedText(
                    "requested_viaticos",
                    "$",
                    css_class="form-group text-right col-md-6",
                ),
                HTML("</td>"),
                HTML("</tr>"),
                HTML("<tr>"),
                HTML('<th scope="row">Otros</th>'),
                HTML("<td>"),
                PrependedText(
                    "total_otros", "$", css_class="form-group text-right col-md-6"
                ),
                HTML("</td>"),
                HTML("<td>"),
                PrependedText(
                    "requested_otros", "$", css_class="form-group text-right col-md-6"
                ),
                HTML("</td>"),
                HTML("</tr>"),
                HTML("</tbody>"),
                HTML("</table>"),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("personal_statement"), css_class="form-group col-md-8 mb-1"
                ),
                css_class="form-row",
            ),
            Row(
                Column(Field("suitability"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("future_plans"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                Column(Field("importance"), css_class="form-group col-md-8 mb-1"),
                css_class="form-row",
            ),
            Row(
                HTML(
                    "<p>Complete el siguiente texto donde exprese los motivos personales por los cuales usted está solicitando el apoyo del programa de fomento a talentos en la Modalidad de Apoyos Directos y Estímulos correspondiente, considerando los puntos que a continuación se describen dentro de la redacción general.</p>"
                ),
            ),
            Row(
                Column(
                    Field("statement_of_purpose"), css_class="form-group col-md-8 mb-1"
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("program_relation_cti"), css_class="form-group col-md-8 mb-1"
                ),
                css_class="form-row",
            ),
            Row(
                Column(
                    Field("program_relation_state"),
                    css_class="form-group col-md-8 mb-1",
                ),
                css_class="form-row",
            ),
            FormActions(
                Submit("save", "Guardar"),
            ),
        )

    class Meta:
        model = ApplicationContentApoyo
        exclude = ("validated", "id")
        widgets = {
            "date_start": forms.SelectDateWidget(
                years=range(datetime.now().year - 5, datetime.now().year + 5, 1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
            "date_end": forms.SelectDateWidget(
                years=range(datetime.now().year - 5, datetime.now().year + 5, 1),
                attrs=({"style": "width: 33%; display: inline-block;"}),
            ),
        }


class AwardDeliverableForm(ModelForm):
    deliverable = forms.FileField(required=True, widget=forms.FileInput, label="Comprobante / Entregable")

    class Meta:
        model = Award
        fields = ["deliverable", ]
