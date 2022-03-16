from django.db import models


class ApplicationFormTemplate(models.Model):
    title = models.CharField("Nombre", max_length=64)
    template = models.TextField("Forma de aplicación (HTML)")

    def __str__(self):
        return self.title


class Program(models.Model):
    application_prefix = models.CharField("Código", max_length=8, unique=True)
    title = models.CharField("Nombre", max_length=64)
    description = models.CharField("Descripción", max_length=512)
    application_form = models.ForeignKey(
        to=ApplicationFormTemplate,
        on_delete=models.CASCADE,
        verbose_name="Formato de aplicación",

    )
    start_date = models.DateField("Fecha de apertura")
    end_date = models.DateField("Fecha de cierre", null=True, blank=True)
    results_date = models.DateField("Publicación de resultados", null=True, blank=True)
    publicity = models.BooleanField("Mostrar a aplicantes")
    no_close_date = models.BooleanField("Programa permanente (sin fecha de cierre)")
    total_awards = models.IntegerField("Número de becas presupuestadas", null=True, blank=True)
    allocated_awards = models.IntegerField("Número de becas asignadas", null=True, blank=True)
    total_budget = models.IntegerField("Presupuesto total", null=True, blank=True)
    allocated_budget = models.IntegerField("Presupuesto asignado a aplicantes", null=True, blank=True)
    paid_budget = models.IntegerField("Presupuesto pagado a aplicantes", null=True, blank=True)
    file = models.FileField("Reglas de operación o convocatoria (pdf)", upload_to="programs/",
                            null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.application_prefix, self.title)
