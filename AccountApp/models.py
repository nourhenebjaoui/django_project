from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# Validation : la date doit être dans le passé
def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("La date doit être dans le passé.")


# Modèle utilisateur
class User(AbstractUser):
    pass


# Modèle spécialité
class Specialty(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name


# Modèle docteur
class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )

    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    specialties = models.ManyToManyField(
        Specialty,
        related_name='doctors'
    )

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return self.username


# Modèle patient
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

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return self.username