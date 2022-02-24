from django.views.generic import TemplateView


class ApplicationsListView(TemplateView):
    template_name = "applications.html"
