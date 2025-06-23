from django.db import models
from django.core.exceptions import ValidationError
from datetime import time

class EventType(models.Model):
    event_type_name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del Tipo de Evento"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    def __str__(self):
        return self.event_type_name
    
    class Meta:
        verbose_name = "Tipo de Evento"
        verbose_name_plural = "Tipos de Eventos"
        ordering = ['event_type_name']

class Department(models.Model):
    department_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.department_name
    
    class Meta:
        verbose_name = "Secretaría/Departamento"
        verbose_name_plural = "Secretarías/Departamentos"
        ordering = ['department_name']

class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    phone_number = models.CharField(max_length=15, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['name']

class Event(models.Model):
    event_name = models.CharField(max_length=150, verbose_name="Nombre del Evento")
    event_type = models.ForeignKey(
        EventType, 
        on_delete=models.CASCADE,
        verbose_name="Tipo de Evento"
    )
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,
        verbose_name="Secretaría"
    )
    start_time = models.DateTimeField(verbose_name="Hora de Inicio")
    end_time = models.DateTimeField(verbose_name="Hora de Fin")
    location = models.CharField(max_length=255, verbose_name="Lugar")
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        verbose_name="Enlace/Contacto de Seguimiento"
    )
    observations = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Observaciones"
    )
    
    def clean(self):
        super().clean()
        
        # Validar horarios permitidos (6:00 AM a 11:59 PM)
        if self.start_time:
            start_hour = self.start_time.time()
            if start_hour < time(6, 0) or start_hour >= time(24, 0):
                raise ValidationError({
                    'start_time': 'Los eventos solo pueden programarse entre las 6:00 AM y las 11:59 PM'
                })
        
        if self.end_time:
            end_hour = self.end_time.time()
            if end_hour < time(6, 0) or end_hour >= time(24, 0):
                raise ValidationError({
                    'end_time': 'Los eventos solo pueden programarse entre las 6:00 AM y las 11:59 PM'
                })
        
        # Validar que la hora de fin sea posterior a la de inicio
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': 'La hora de fin debe ser posterior a la hora de inicio'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.event_name} - {self.start_time.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['start_time']
        
class AdditionalObservation(models.Model):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name='additional_observations'
    )
    observation_text = models.TextField(verbose_name="Observación")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Observación para {self.event.event_name}: {self.observation_text[:50]}..."
    
    class Meta:
        verbose_name = "Observación Adicional"
        verbose_name_plural = "Observaciones Adicionales"
        ordering = ['-created_at']