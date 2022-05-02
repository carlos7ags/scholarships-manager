from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import UserCreationForm

from actions.utils import auto_assign_tasks_at_user_creation


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "user_registration.html"

    def form_valid(self, form):
        self.object = form.save()
        auto_assign_tasks_at_user_creation(self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("applicant-dashboard")
