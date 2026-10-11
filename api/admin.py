from django.contrib import admin

from .models import Lugar, Persona, Viaje


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'email', 'fecha_nacimiento')
    search_fields = ('rut', 'nombre', 'apellido', 'email')
    list_filter = ('fecha_nacimiento',)


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'pais')
    search_fields = ('nombre', 'ciudad', 'pais')


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'persona', 'lugar', 'fecha_visita', 'calificacion', 'creado')
    list_filter = ('calificacion', 'lugar', 'fecha_visita')
    search_fields = ('titulo', 'relato', 'persona__nombre', 'lugar__nombre')
    date_hierarchy = 'creado'
