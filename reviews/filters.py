import django_filters

from applications.models import Application, Award
from programs.models import Program


class ApplicationsFilter(django_filters.FilterSet):
    program = django_filters.ModelChoiceFilter(
        queryset=Program.objects.all(),
    )
    current_stage = django_filters.ChoiceFilter(
        choices=Application.APPLICATION_STAGES,
    )
    decision__decision = django_filters.ChoiceFilter(
        choices=Award.AWARD_STATUS,
    )

    class Meta:
        model = Application
        fields = {
            "username__username": ["icontains"],
            "folio": ["icontains"],
        }
