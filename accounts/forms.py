from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import CharField, EmailField


class UserCreationForm(UserCreationForm):
    email = EmailField(label=("Correo electrónico"), required=True)
    username = CharField(
        label="CURP",
        help_text="Para registrar un nuevo usario ingresa tu CURP (utiliza letras mayúsculas).",
        max_length=18,
        validators=[
            RegexValidator(
                regex=r"([A-z]{4}[0-9]{6}[HMhm]{1}[A-z]{5}[0-z]{1}[0-9]{1})",
                message="Ingresa una CURP válida.",
                code="invalid_curp",
            ),
            RegexValidator(
                regex=r"^[A-Z0-9]*$",
                message="Utiliza letras mayúsculas y números.",
                code="invalid_curp",
            ),
        ],
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
