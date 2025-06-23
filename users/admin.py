# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "nombre_completo", "is_staff")
    ordering = ("email",)
    search_fields = ("email", "nombre_completo")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("nombre_completo", "telefono")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nombre_completo", "telefono", "password1", "password2", "is_staff", "is_active"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
