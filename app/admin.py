from django.contrib import admin

from .models import Asignatura, Calificacion, Estudiante, Evaluacion


@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'creditos', 'creada_en')
    search_fields = ('codigo', 'nombre')


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'correo', 'fecha_nacimiento')
    search_fields = ('rut', 'nombres', 'apellidos', 'correo')
    filter_horizontal = ('asignaturas',)


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'asignatura', 'tipo', 'fecha', 'puntaje_maximo', 'ponderacion')
    list_filter = ('tipo', 'asignatura')
    search_fields = ('titulo', 'asignatura__nombre')
    date_hierarchy = 'fecha'


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'evaluacion', 'puntaje', 'observaciones', 'registrada_en')
    list_filter = ('evaluacion__asignatura', 'evaluacion')
    search_fields = ('estudiante__nombres', 'estudiante__apellidos', 'estudiante__rut')
