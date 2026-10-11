from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Lugar, Persona, Viaje
from .serializers import LugarSerializer, PersonaSerializer, ViajeSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    """CRUD completo de personas."""

    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    lookup_value_regex = r'\d+'


class LugarViewSet(viewsets.ModelViewSet):
    """CRUD completo de lugares, con listado de viajes por lugar."""

    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer
    lookup_value_regex = r'\d+'

    @action(detail=True, methods=['get'])
    def viajes(self, request, pk=None):
        """Retorna los viajes registrados en el lugar: /api/lugares/<id>/viajes/"""
        lugar = self.get_object()
        viajes = Viaje.objects.filter(lugar=lugar).select_related('persona', 'lugar')
        serializer = ViajeSerializer(viajes, many=True)
        return Response(serializer.data)


class ViajeViewSet(viewsets.ModelViewSet):
    """CRUD de viajes con filtrado opcional por ?lugar= y ?persona=."""

    queryset = Viaje.objects.select_related('persona', 'lugar')
    serializer_class = ViajeSerializer
    lookup_value_regex = r'\d+'

    def get_queryset(self):
        queryset = Viaje.objects.select_related('persona', 'lugar')
        lugar = self.request.query_params.get('lugar')
        persona = self.request.query_params.get('persona')
        if lugar is not None:
            queryset = queryset.filter(lugar_id=lugar) if lugar.isdigit() else queryset.none()
        if persona is not None:
            queryset = queryset.filter(persona_id=persona) if persona.isdigit() else queryset.none()
        return queryset
