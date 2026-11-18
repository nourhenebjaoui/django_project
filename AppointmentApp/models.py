from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE
    )

    appointment_date = models.DateTimeField()

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(['pdf'])]
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.appointment_date:
            if self._state.adding:
                if self.appointment_date <= timezone.now():
                    raise ValidationError({
                        'appointment_date': 'Appointment date must be in the future.'
                    })

            else:
                old_date = Appointment.objects.filter(
                    pk=self.pk
                ).values_list('appointment_date', flat=True).first()

                if old_date != self.appointment_date:
                    if self.appointment_date <= timezone.now():
                        raise ValidationError({
                            'appointment_date': 'Appointment date must be in the future.'
                        })

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]