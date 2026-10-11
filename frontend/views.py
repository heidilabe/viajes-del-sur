from django.shortcuts import render
from django.urls import reverse


def blog(request):
    """Renderiza el listado de viajes (los datos se cargan con fetch desde la API)."""
    return render(request, 'frontend/blog.html')


def login_view(request):
    """Renderiza el formulario de inicio de sesión."""
    return render(request, 'frontend/login.html')


def detalle_viaje(request, pk):
    """Renderiza la plantilla del detalle; el viaje se consume desde /api/viajes/<pk>/."""
    return render(request, 'frontend/detalle_viaje.html', {'pk': pk})


# --- Viajes ---

def crear_viaje(request):
    """Renderiza el formulario de creación de viajes."""
    return render(request, 'frontend/form_viaje.html')


def editar_viaje(request, pk):
    """Renderiza el formulario de edición del viaje <pk>."""
    return render(request, 'frontend/form_viaje.html', {'pk': pk})


def eliminar_viaje(request, pk):
    """Renderiza la confirmación para eliminar el viaje <pk>."""
    return render(request, 'frontend/confirmar_eliminar.html', {
        'titulo': 'Eliminar Viaje',
        'api_url': f'/api/viajes/{pk}/',
        'volver_url': reverse('blog'),
        'volver_texto': 'Volver al Blog',
    })


# --- Personas ---

def lista_personas(request):
    """Renderiza la tabla de personas."""
    return render(request, 'frontend/personas.html')


def crear_persona(request):
    """Renderiza el formulario de creación de personas."""
    return render(request, 'frontend/form_persona.html')


def editar_persona(request, pk):
    """Renderiza el formulario de edición de la persona <pk>."""
    return render(request, 'frontend/form_persona.html', {'pk': pk})


def eliminar_persona(request, pk):
    """Renderiza la confirmación para eliminar la persona <pk>."""
    return render(request, 'frontend/confirmar_eliminar.html', {
        'titulo': 'Eliminar Persona',
        'api_url': f'/api/personas/{pk}/',
        'volver_url': reverse('lista_personas'),
        'volver_texto': 'Volver a Personas',
    })


# --- Lugares ---

def lista_lugares(request):
    """Renderiza el listado de lugares."""
    return render(request, 'frontend/lugares.html')


def crear_lugar(request):
    """Renderiza el formulario de creación de lugares."""
    return render(request, 'frontend/form_lugar.html')


def editar_lugar(request, pk):
    """Renderiza el formulario de edición del lugar <pk>."""
    return render(request, 'frontend/form_lugar.html', {'pk': pk})


def eliminar_lugar(request, pk):
    """Renderiza la confirmación para eliminar el lugar <pk>."""
    return render(request, 'frontend/confirmar_eliminar.html', {
        'titulo': 'Eliminar Lugar',
        'api_url': f'/api/lugares/{pk}/',
        'volver_url': reverse('lista_lugares'),
        'volver_texto': 'Volver a Lugares',
    })
