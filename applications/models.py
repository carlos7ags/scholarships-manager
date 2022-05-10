from django.db import models
from programs.models import Program
from django.conf import settings


class Award(models.Model):
    AWARD_STATUS = ((0, "Rechazado"), (1, "Aprobado"))

    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Solicitante",
    )
    program = models.ForeignKey(
        to=Program,
        on_delete=models.CASCADE,
        verbose_name="Programa",
    )
    decision = models.IntegerField(
        "Decisión",
        choices=AWARD_STATUS,
        null=True,
    )
    awarded = models.IntegerField("Monto autorizado", default=0, null=True, blank=True)
    comments = models.TextField("Comentarios", null=True, blank=True)
    acta = models.TextField("Número de acta", null=True, blank=True)
    require_deliverable = models.BooleanField("Requiere entregables", default=False)
    deliverable_by = models.DateTimeField("Fecha para entregables", null=True)
    deliverable = models.FileField("Entregable", null=True, blank=True)
    deliverable_validated = models.BooleanField("Entregable validado", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.program, self.username)


"""
class DirectAwardApplicationForm(models.Model):
    AWARD_STATUS = ((0, "Rechazado"), (1, "Aprobado"))

    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Solicitante",
    )
    program = models.ForeignKey(
        to=Program,
        on_delete=models.CASCADE,
        verbose_name="Programa",
    )

    start_date = models.DateField("Fecha de Inicio de estudios, especialidad, posgrado o actividad académica para la cuál requiere el apoyo.")
    end_date = models.DateField("Fecha de término de estudios, especialidad, Posgrado o actividad académica para la cuál requiere el apoyo.", null=True, blank=True)
    program_name = models.CharField("Nombre de los estudios o actividad que realizará y para la cuál pide el apoyo.", max_length=100)
    program_objective = models.TextField("Objetivo de los estudios o actividad que realizará y para la cuál pide el apoyo.")
    program_area = models.CharField("Área o perfil de los estudios o actividad que realizará y para la cuál pide el apoyo.", max_length=100)
    program_institution = models.CharField("Institución donde realizará sus estudios o actividad.", max_length=100)
    program_location = models.CharField("Ciudad o país donde realizará sus estudios o actividad.", max_length=100)

    current_institution = models.CharField("Institución o empresa donde estudia o trabaja actualmente.", max_length=100)
    last_program = models.CharField("Último grado académico o módulo cursado.", max_length=100)
    last_grade = models.CharField("Promedio último obtenido / equivalencia (con documento oficial institucional si es correspondiente al extranjero, solo aplica para modalidad por convocatoria)", max_length=100)
    other = models.TextField("Otros.")

    total_movilidad = models.IntegerField("")
    requested_movilidad = models.IntegerField("")
    total_investigacion = models.IntegerField("")
    requested_investigacion = models.IntegerField("")
    total_inscripcion = models.IntegerField("")
    requested_inscripcion = models.IntegerField("")
    total_viaicos = models.IntegerField("")
    requested_viaticos = models.IntegerField("")
    total_otros = models.IntegerField("")
    requested_otros = models.IntegerField("")

    personal_statement = models.TextField("Objetivo personal que lo impulsó para seguir estudiando.")
    suitability = models.TextField("Diga, ¿por qué es pertinente el apoyar su formación en la modalidad pretendida?")
    future_plans = models.TextField("Planes de trabajo después de terminar sus estudios.")
    importance = models.TextField("Fundamente las ventajas de esta institución y programa sobre la oferta educativa en Aguascalientes.")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.program, self.username)
"""


class Application(models.Model):
    APPLICATION_STAGES = (
        (0, "Pendiente"),
        (1, "Enviada"),
        (2, "En revisión"),
        (3, "Validada"),
        (4, "Decisión final"),
        (5, "Seguimiento"),
        (6, "Concluida"),
        (-1, "Cancelada"),
    )

    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Solicitante",
    )
    program = models.ForeignKey(
        to=Program,
        on_delete=models.CASCADE,
        verbose_name="Programa",
    )
    folio = models.CharField("Folio", unique=True, max_length=256)
    current_stage = models.IntegerField(
        "Estatus",
        choices=APPLICATION_STAGES,
        default=0,
    )
    application_form = models.JSONField(null=True, blank=True)
    score = models.CharField("Puntuación", max_length=64, null=True, blank=True)
    decision = models.ForeignKey(
        to=Award,
        on_delete=models.CASCADE,
        verbose_name="Decisión",
        null=True,
        blank=True,
    )
    validated = models.BooleanField(default=False)
    comments = models.TextField("Comentarios", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            (
                "program",
                "username",
            ),
        )

    def __str__(self):
        return "%s - %s - %s" % (self.program, self.folio, self.username)
