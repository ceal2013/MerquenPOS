from django.urls import path
from . import views

urlpatterns = [
    path('mesas/', views.seleccion_mesas_view, name='seleccion_mesas'),
    path('mesa/<str:punto>/<str:numero>/', views.abrir_mesa_view, name='abrir_mesa'),
    
   # Endpoints AJAX para la Comanda
    path('api/ticket/agregar/', views.api_agregar_ticket, name='api_agregar_ticket'),
    path('api/ticket/borrar/', views.api_borrar_ticket, name='api_borrar_ticket'),
    path('api/ticket/comandar/', views.api_comandar_ticket, name='api_comandar_ticket'),
    path('api/ticket/anular/', views.api_anular_ticket, name='api_anular_ticket'),
]