from datetime import date

from rest_framework import serializers

from .models import Lugar, Persona, Viaje


class PersonaSerializer(serializers.ModelSerializer):
    cantidad_viajes = serializers.SerializerMethodField()

    class Meta:
        model = Persona
        fields = [
            'id',
            'rut',
            'nombre',
            'apellido',
            'email',
            'fecha_nacimiento',
            'foto',
            'cantidad_viajes',
        ]

    def get_cantidad_viajes(self, obj):
        return obj.viajes.count()

    def validate_fecha_nacimiento(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value


class LugarSerializer(serializers.ModelSerializer):
    cantidad_visitas = serializers.SerializerMethodField()
    promedio_calificacion = serializers.SerializerMethodField()

    class Meta:
        model = Lugar
        fields = [
            'id',
            'nombre',
            'pais',
            'ciudad',
            'descripcion',
            'foto',
            'cantidad_visitas',
            'promedio_calificacion',
        ]

    def get_cantidad_visitas(self, obj):
        return obj.viajes.count()

    def get_promedio_calificacion(self, obj):
        valoraciones = [v.calificacion for v in obj.viajes.all()]
        if not valoraciones:
            return None
        return round(sum(valoraciones) / len(valoraciones), 2)


class ViajeSerializer(serializers.ModelSerializer):
    persona_detalle = PersonaSerializer(source='persona', read_only=True)
    lugar_detalle = LugarSerializer(source='lugar', read_only=True)

    class Meta:
        model = Viaje
        fields = [
            'id',
            'persona',
            'lugar',
            'fecha_visita',
            'titulo',
            'relato',
            'foto',
            'calificacion',
            'creado',
            'persona_detalle',
            'lugar_detalle',
        ]

    def validate_fecha_visita(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de visita no puede ser futura.")
        return value

    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5.")
        return value
