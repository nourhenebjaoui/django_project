
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient, Specialty
from AppointmentApp.models import Appointment


admin.site.register(User, UserAdmin)


class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    fields = (
        'patient',
        'appointment_date',
        'reason',
        'status',
        'duration_minutes',
    )
    readonly_fields = (
        'patient',
        'appointment_date',
        'reason',
        'status',
        'duration_minutes',
    )
    can_delete = False


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'password',
        'first_name',
        'last_name',
        'email',
        'license_number',
        'phone',
        'specialties',
    )
    inlines = [AppointmentInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['license_number']
        return []


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'password',
        'first_name',
        'last_name',
        'email',
        'national_id',
        'phone',
        'birth_date',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['national_id']
        return []


admin.site.register(Specialty)
