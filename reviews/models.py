from django.db import models

from django.conf import settings

from programs.models import Program


class ReviewersProgramACL(models.Model):
    username = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    program = models.ForeignKey(
        to=Program,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Username: %s - Program: %s" % (self.username, self.program.application_prefix)
