import django_filters

from actions.models import PendingTasks
from applications.models import Application, Award
from programs.models import Program


class ApplicationsFilter(django_filters.FilterSet):
    program = django_filters.ModelChoiceFilter(
        queryset=Program.objects.all(),
    )
    current_stage = django_filters.ChoiceFilter(
        choices=Application.APPLICATION_STAGES,
    )

    class Meta:
        model = Application
        fields = {
            "username__username": ["icontains"],
            "folio": ["icontains"],
        }


class AwardsFilter(django_filters.FilterSet):
    program = django_filters.ModelChoiceFilter(
        queryset=Program.objects.all(),
    )

    decision = django_filters.ChoiceFilter(
        choices=Award.AWARD_STATUS, label="Decisión"
    )

    deliverable_validated = django_filters.BooleanFilter("deliverable_validated", label="Comprobante entregado")
    award_delivered = django_filters.BooleanFilter("award_delivered", label="Apoyo entregado")

    class Meta:
        model = Award
        fields = {
            "username__username": ["icontains"],
        }


class PendingTasksFilter(django_filters.FilterSet):

    class Meta:
        model = PendingTasks
        fields = {
            "username__username": ["icontains"],
        }
