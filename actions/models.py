from django.db import models

from django.conf import settings


class TaskType(models.Model):
    TASK_TYPE = ((0, "Formulario"), (1, "Archivo"))

    name = models.CharField("Nombre", max_length=100)
    message = models.CharField("Mensaje a mostrar", max_length=250)
    instructions = models.CharField("Instrucciones", max_length=1000)
    type = models.IntegerField(
        "Tipo de tarea",
        choices=TASK_TYPE,
    )
    required_to_apply = models.BooleanField("", default=True)
    has_deadline = models.BooleanField("Tiene fecha límite", default=False)
    days_to_complete = models.IntegerField("Días para completar", default=30)
    redirect_to = models.CharField("Redirigir a", max_length=200)


class PendingTasks(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Solicitante",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        verbose_name="Tipo de tarea",
    )
    deadline = models.DateTimeField("Fecha límite")
    completed = models.BooleanField("Completada", default=False)


    def __str__(self):
        return "%s - %s - %s" % (self.username, self.task_type, self.deadline)
