from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("Birth date must be in the past.")


class User(AbstractUser):
    pass


class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )


class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    birth_date = models.DateField(
        validators=[validate_past_date]
    )


class Specialty(models.Model):
    name = models.CharField(max_length=100)
    doctors = models.ManyToManyField(
        Doctor,
        related_name="specialties"
    )