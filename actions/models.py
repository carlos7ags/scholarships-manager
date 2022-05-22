from django.db import models

from django.conf import settings


class Task(models.Model):
    TASK_TYPE = ((0, "Formulario"), (1, "Archivo"), (2, "Presencial"),)

    name = models.CharField("Nombre", max_length=100)
    message = models.CharField("Mensaje a mostrar", max_length=250)
    instructions = models.CharField("Instrucciones", max_length=1000)
    type = models.IntegerField(
        "Tipo de tarea",
        choices=TASK_TYPE,
    )
    has_deadline = models.BooleanField("Tiene fecha límite", default=False)
    days_to_complete = models.IntegerField("Días para completar", default=30)
    required_to_apply = models.BooleanField("Necesario para aplicar", default=True)
    auto_create_at_user_init = models.BooleanField("Autoasignar al crear usuario", default=False)
    has_next_task = models.BooleanField("Tiene siguiente tarea", default=False)
    next_task = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    has_redirect_url = models.BooleanField("Tiene url para redirigir", default=False)
    redirect_url = models.CharField("Url para redirigir", max_length=1000, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.get_type_display(), self.name)


class PendingTasks(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Solicitante",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Tarea",
    )
    comments = models.TextField("Comentarios", blank=True, null=True)
    redirect_url_overwrite = models.TextField("Url para redirigir (específica)", blank=True, null=True)
    deadline = models.DateTimeField("Fecha límite", blank=True, null=True)
    completed = models.BooleanField("Completada", default=False)

    def __str__(self):
        return "%s - %s" % (self.username, self.task)
