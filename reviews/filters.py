import django_filters

from applications.models import Application
from programs.models import Program


class ApplicationsFilter(django_filters.FilterSet):
    program = django_filters.ModelChoiceFilter(
        queryset=Program.objects.all()
    )
    
    class Meta:
        model = Application
        fields = {
            "username__username": ["icontains"],
            "folio": ["icontains"],
        }
