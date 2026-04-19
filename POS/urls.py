from django.urls import path
from . import views

urlpatterns = [
    path('mesas/', views.seleccion_mesas_view, name='seleccion_mesas'),
    path('mesa/<str:punto>/<str:numero>/', views.abrir_mesa_view, name='abrir_mesa'),
    
    path('comanda/<str:punto>/<str:numero>/<str:folio>/', views.comanda_view, name='comanda'),
    path('api/grupos/<str:punto>/<str:clase>/', views.api_get_grupos, name='api_grupos'),
    path('api/productos/<str:punto>/<str:clase>/<str:grupo>/', views.api_get_productos, name='api_productos'),
]