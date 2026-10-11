from django.urls import path

from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('login/', views.login_view, name='login'),

    path('viajes/nuevo/', views.crear_viaje, name='crear_viaje'),
    path('viajes/<int:pk>/', views.detalle_viaje, name='detalle_viaje'),
    path('viajes/<int:pk>/editar/', views.editar_viaje, name='editar_viaje'),
    path('viajes/<int:pk>/eliminar/', views.eliminar_viaje, name='eliminar_viaje'),

    path('personas/', views.lista_personas, name='lista_personas'),
    path('personas/nueva/', views.crear_persona, name='crear_persona'),
    path('personas/<int:pk>/editar/', views.editar_persona, name='editar_persona'),
    path('personas/<int:pk>/eliminar/', views.eliminar_persona, name='eliminar_persona'),

    path('lugares/', views.lista_lugares, name='lista_lugares'),
    path('lugares/nuevo/', views.crear_lugar, name='crear_lugar'),
    path('lugares/<int:pk>/editar/', views.editar_lugar, name='editar_lugar'),
    path('lugares/<int:pk>/eliminar/', views.eliminar_lugar, name='eliminar_lugar'),
]
