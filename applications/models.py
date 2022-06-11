from django.conf import settings
from django.db import models

from programs.models import Program


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


class ApplicationContentConvocatoria(models.Model):
    id = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_start = models.DateField(verbose_name="Fecha de inicio del programa")
    date_end = models.DateField(verbose_name="Fecha de término del programa")
    program_description = models.TextField(
        verbose_name="Descripción del programa, tema de estudio o actividad académica que pretende realizar"
    )


class ApplicationContentApoyo(models.Model):

    LANGUAGES = (
        ("spanish", "Español"),
        ("english", "Inglés"),
        ("portuguese", "Portugués"),
        ("french", "Francés"),
        ("french", "Otro"),
    )

    id = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_start = models.DateField(verbose_name="Fecha de inicio del programa")
    date_end = models.DateField(verbose_name="Fecha de término del programa")
    name = models.CharField(
        verbose_name="Nombre del programa de estudios", max_length=120
    )
    description = models.TextField(
        verbose_name="Descripción del programa, tema de estudio o actividad académica que pretende realizar"
    )
    objective = models.TextField("Objetivo de los estudios o actividad que realizará y para la cuál pide el apoyo")
    credits = models.IntegerField("Número de asignaturas o créditos del programa")
    duration_hours = models.IntegerField("Duración del programa de estudios (horas)")
    language = models.CharField("Idioma en que se imparte el programa",
                                choices=LANGUAGES,
                                max_length=50,
                                )
    area = models.CharField("Área del programa", max_length=100)
    impact = models.TextField("Impacto y beneficios del programa para el estado")
    institution = models.CharField("Institución donde realizará sus estudios o actividad", max_length=100)
    location = models.CharField("Ciudad o país donde realizará sus estudios o actividad", max_length=100)
    materias = models.TextField("Lista de materias y número de créditos", help_text="Sólo en caso de estar matriculado y cursando un programa de doctorado o maestría. Inserte una materia por renglon con el número de créditos separado con una coma, por ejemplo:<br/>Matemáticas, 4<br/>Español, 4<br/>Ciencias Naturales, 6")
    research_topic = models.CharField("Línea de investigación", max_length=400, help_text="Solo en caso de estar matriculado y cursando programa de doctorado o maestría.")
    program_requirements = models.CharField("Link al programa de estudios", max_length=400, help_text="Enlace o link o nombre del documento donde se pueda verificar la información de la estructura curricular y las líneas de investigación. Si la información se encuentra en un documento entregado en su expediente, indicar los números de página en donde se ubica.")

    total_movilidad = models.IntegerField("", default=0)
    requested_movilidad = models.IntegerField("", default=0)
    total_investigacion = models.IntegerField("", default=0)
    requested_investigacion = models.IntegerField("", default=0)
    total_inscripcion = models.IntegerField("", default=0)
    requested_inscripcion = models.IntegerField("", default=0)
    total_viaticos = models.IntegerField("", default=0)
    requested_viaticos = models.IntegerField("", default=0)
    total_otros = models.IntegerField("", default=0)
    requested_otros = models.IntegerField("", default=0)

    personal_statement = models.TextField("Objetivo personal que lo impulsó para seguir estudiando")
    suitability = models.TextField("Explique, ¿por qué es pertinente el apoyar su formación en la modalidad pretendida?")
    future_plans = models.TextField("Planes de trabajo después de terminar sus estudios")
    importance = models.TextField("Fundamente las ventajas de esta institución y programa sobre la oferta educativa en Aguascalientes")
    statement_of_purpose = models.TextField("Exposición de motivos", default="Me dirijo a usted de la manera más atenta para solicitarle...\n\nObjetivo...\n\nMotivo de solicitud...\n\nBeneficios e impacto que tendrá realizar sus estudios o actividad para la cual requiere el apoyo...\n")
    program_relation_cti = models.TextField("Señale la relación del proyecto de estudios con los sectores estratégicos y el impacto o beneficios para el Estado")
    program_relation_state = models.TextField("Argumetación sobre la relación del proyecto o programa de estudios con la ciencia, la tecnología y la innovación")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s - %s" % (self.id, self.id.username, self.id.program)
