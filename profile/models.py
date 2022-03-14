import os
from uuid import uuid4

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image
from encrypted_model_fields.fields import EncryptedCharField


def path_and_rename(instance, filename):
    upload_to = "photos"
    ext = filename.split(".")[-1]
    # set filename as random string
    filename = "{}.{}".format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    """Información personal"""

    GENDER_CHOICES = (
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
    )

    MARITAL_STATUS_CHOICES = (
        ('soltero', 'Soltero'),
        ('casado', 'Casado'),
    )

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )

    name = models.CharField("Nombre(s)", max_length=25)
    lastname_first = models.CharField("Apellido paterno", max_length=15)
    lastname_second = models.CharField(
        "Apellido materno", max_length=15, null=True, blank=True
    )

    birthday = models.DateField("Fecha de nacimiento")

    birth_place = models.CharField(
        "Lugar de nacimiento",
        max_length=30,
    )

    nationality = models.CharField("Nacionalidad", max_length=15)

    curp = models.CharField(
        "CURP",
        max_length=18,
        validators=[
            RegexValidator(
                regex=r"([A-z]{4}[0-9]{6}[HMhm]{1}[A-z]{5}[0-z]{1}[0-9]{1})",
                message="Ingresa una CURP válida.",
                code="invalid_curp",
            ),
        ], null=True, blank=True,
    )

    ine = models.CharField(
        "INE",
        max_length=13,
        null=True,
        blank=True,
        help_text='Registra los 13 digitos que siguen a los simbolos "<<" en la parte posterior de tu INE.',
        validators=[
            RegexValidator(
                regex=r"([0-9]{13})",
                message="Ingresa una clave INE válida.",
                code="invalid_ine",
            )
        ],
    )

    passport = models.CharField("Pasaporte", max_length=15, null=True, blank=True,)

    marital_status = models.CharField(
        "Estado civil",
        choices=MARITAL_STATUS_CHOICES,
        max_length=15,
    )

    gender = models.CharField(
        "Género",
        choices=GENDER_CHOICES,
        max_length=15,
    )

    occupation = models.CharField("Ocupación", max_length=25)

    validated = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        "Foto de perfil",
        upload_to=path_and_rename,
        null=False,
        blank=False,
        help_text="Esta fotografía se integrará a la solicitud y expendiente. Se requiere fotografía tipo pasaporte.",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_picture.path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    def __str__(self):
        return "%s - %s" % (self.username, self.curp)


class Address(models.Model):
    """Dirección"""

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )

    street = models.CharField("Calle", max_length=100)

    exterior_number = models.IntegerField("Número exterior")

    interior_number = models.IntegerField("Número interior", null=True, blank=True)

    suburb = models.CharField("Colonia", max_length=100)

    postal_code = models.IntegerField(
        "Código postal",
        validators=[
            RegexValidator(
                regex=r"([0-9]{5})",
                message="Ingresa un código postal valido.",
                code="invalid_postal_code",
            )
        ],
    )

    locality = models.CharField("Localidad", max_length=100)

    municipality = models.CharField(
        "Municipio o delegación",
        max_length=30,
    )

    state = models.CharField(
        "Estado",
        max_length=30,
    )

    validated = models.BooleanField(default=False)

    def __str__(self):
        return "Address for %s" % (self.username)


class Contact(models.Model):
    """Datos de contacto"""

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )

    phone = models.CharField(
        "Teléfono fijo",
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"([0-9]{10})",
                message="Ingresa un teléfono válido de 10 dígitos.",
                code="invalid_phone",
            )
        ],
    )

    mobile = models.CharField(
        "Celular",
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"([0-9]{10})",
                message="Ingresa un teléfono válido de 10 digitos.",
                code="invalid_phone",
            )
        ],
    )

    email = models.EmailField("Correo electrónico")

    validated = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.username, self.email)


class EmergencyContact(models.Model):

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )

    name = models.CharField("Nombre del contacto", max_length=100)
    phone = models.CharField(
        "Teléfono fijo",
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"([0-9]{10})",
                message="Ingresa un teléfono válido de 10 dígitos.",
                code="invalid_phone",
            )
        ],
    )

    mobile = models.CharField(
        "Celular",
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"([0-9]{10})",
                message="Ingresa un teléfono válido de 10 digitos.",
                code="invalid_phone",
            )
        ],
    )
    address = models.CharField("Dirección", max_length=100)
    location = models.CharField("Ciudad y pais", max_length=75)

    email = models.EmailField("Correo electrónico")

    validated = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.username, self.email)


class Bank(models.Model):
    """Datos bancarios"""

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        primary_key=True,
    )

    bank_name = EncryptedCharField(
        "Nombre del banco",
        max_length=100,
    )

    account_number = EncryptedCharField(
        "Número de cuenta",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"[0-9]{18}",
                message="Ingresa un número de cuenta válido de 20 dígitos.",
                code="invalid_phone",
            )
        ],
    )

    clabe = EncryptedCharField(
        "CLABE",
        max_length=18,
        validators=[
            RegexValidator(
                regex=r"[0-9]{18}",
                message="Ingresa un número CLABE válido de 18 dígitos.",
                code="invalid_phone",
            )
        ],
    )

    validated = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.username, self.bank_name)
