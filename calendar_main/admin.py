from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Event, EventType, Department, Contact, AdditionalObservation

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('event_type_name', 'is_active', 'description_preview')
    list_filter = ('is_active',)
    search_fields = ('event_type_name', 'description')
    list_editable = ('is_active',)
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "Sin descripción"
    description_preview.short_description = "Descripción"

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'description_preview', 'events_count')
    search_fields = ('department_name', 'description')
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "Sin descripción"
    description_preview.short_description = "Descripción"
    
    def events_count(self, obj):
        count = obj.event_set.count()
        if count > 0:
            url = reverse('admin:events_event_changelist') + f'?department__id__exact={obj.id}'
            return format_html('<a href="{}">{} eventos</a>', url, count)
        return "0 eventos"
    events_count.short_description = "Eventos"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'events_count')
    search_fields = ('name', 'phone_number', 'email')
    list_filter = ('name',)
    
    def events_count(self, obj):
        count = obj.event_set.count()
        if count > 0:
            url = reverse('admin:events_event_changelist') + f'?contact__id__exact={obj.id}'
            return format_html('<a href="{}">{} eventos</a>', url, count)
        return "0 eventos"
    events_count.short_description = "Eventos"

class AdditionalObservationInline(admin.TabularInline):
    model = AdditionalObservation
    extra = 0
    fields = ('observation_text', 'created_by', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'event_name', 
        'event_type', 
        'department', 
        'formatted_start_time', 
        'formatted_end_time',
        'location_short',
        'contact',
        'status_indicator'
    )
    list_filter = (
        'event_type', 
        'department', 
        'start_time',
        ('start_time', admin.DateFieldListFilter),
    )
    search_fields = (
        'event_name', 
        'location', 
        'contact__name', 
        'department__department_name',
        'event_type__event_type_name'
    )
    date_hierarchy = 'start_time'
    ordering = ('start_time',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('event_name', 'event_type', 'department')
        }),
        ('Horario y Ubicación', {
            'fields': ('start_time', 'end_time', 'location')
        }),
        ('Contacto y Seguimiento', {
            'fields': ('contact', 'observations')
        }),
    )
    
    inlines = [AdditionalObservationInline]
    
    def formatted_start_time(self, obj):
        return obj.start_time.strftime('%d/%m/%Y %H:%M')
    formatted_start_time.short_description = "Inicio"
    formatted_start_time.admin_order_field = 'start_time'
    
    def formatted_end_time(self, obj):
        return obj.end_time.strftime('%d/%m/%Y %H:%M')
    formatted_end_time.short_description = "Fin"
    formatted_end_time.admin_order_field = 'end_time'
    
    def location_short(self, obj):
        return obj.location[:30] + "..." if len(obj.location) > 30 else obj.location
    location_short.short_description = "Lugar"
    
    def status_indicator(self, obj):
        from django.utils import timezone
        now = timezone.now()
        
        if obj.end_time < now:
            return format_html(
                '<span style="color: #666; font-weight: bold;">✓ Finalizado</span>'
            )
        elif obj.start_time <= now <= obj.end_time:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">● En curso</span>'
            )
        else:
            return format_html(
                '<span style="color: #007bff; font-weight: bold;">○ Programado</span>'
            )
    status_indicator.short_description = "Estado"
    
    def get_queryset(self, request):
        # Optimizar consultas con select_related
        return super().get_queryset(request).select_related(
            'event_type', 'department', 'contact'
        )
    
    # Acciones personalizadas
    actions = ['mark_as_completed', 'duplicate_events']
    
    def mark_as_completed(self, request, queryset):
        # Agregar observación de finalización
        for event in queryset:
            AdditionalObservation.objects.get_or_create(
                event=event,
                observation_text="Evento marcado como completado desde el admin",
                created_by=request.user.username if request.user.is_authenticated else "Admin"
            )
        self.message_user(request, f"{queryset.count()} eventos marcados como completados.")
    mark_as_completed.short_description = "Marcar eventos como completados"
    
    def duplicate_events(self, request, queryset):
        duplicated = 0
        for event in queryset:
            # Crear copia del evento
            new_event = Event(
                event_name=f"Copia de {event.event_name}",
                event_type=event.event_type,
                department=event.department,
                start_time=event.start_time,
                end_time=event.end_time,
                location=event.location,
                contact=event.contact,
                observations=event.observations
            )
            new_event.save()
            duplicated += 1
        self.message_user(request, f"{duplicated} eventos duplicados exitosamente.")
    duplicate_events.short_description = "Duplicar eventos seleccionados"

@admin.register(AdditionalObservation)
class AdditionalObservationAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'observation_preview', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('event__event_name', 'observation_text', 'created_by')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    def event_name(self, obj):
        url = reverse('admin:events_event_change', args=[obj.event.id])
        return format_html('<a href="{}">{}</a>', url, obj.event.event_name)
    event_name.short_description = "Evento"
    
    def observation_preview(self, obj):
        return obj.observation_text[:50] + "..." if len(obj.observation_text) > 50 else obj.observation_text
    observation_preview.short_description = "Observación"

# Personalización del admin site
admin.site.site_header = "Sistema de Gestión de Eventos - H. Ayuntamiento de Tapachula"
admin.site.site_title = "Gestión de Eventos"
admin.site.index_title = "Panel de Administración"