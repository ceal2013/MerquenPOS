from django.urls import path
from . import views

urlpatterns = [
    # --- PANTALLAS PRINCIPALES ---
    path('mesas/', views.seleccion_mesas_view, name='seleccion_mesas'),
    path('mesa/<str:punto>/<str:numero>/', views.abrir_mesa_view, name='abrir_mesa'),
    path('comanda/<str:punto>/<str:numero>/<str:folio>/', views.comanda_view, name='comanda'),
    
    # --- ENDPOINTS AJAX (Carga de Menú) ---
    path('api/grupos/<str:punto>/<str:clase>/', views.api_get_grupos, name='api_grupos'),
    path('api/productos/<str:punto>/<str:clase>/<str:grupo>/', views.api_get_productos, name='api_productos'),
    
    # --- ENDPOINTS AJAX (Acciones del Ticket/Comanda) ---
    path('api/ticket/agregar/', views.api_agregar_ticket, name='api_agregar_ticket'),
    path('api/ticket/borrar/', views.api_borrar_ticket, name='api_borrar_ticket'),
    path('api/ticket/comandar/', views.api_comandar_ticket, name='api_comandar_ticket'),
    path('api/ticket/anular/', views.api_anular_ticket, name='api_anular_ticket'),
]