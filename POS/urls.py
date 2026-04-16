from django.urls import path
from . import views

urlpatterns = [
    path('mesas/', views.seleccion_mesas_view, name='seleccion_mesas'),
    path('mesa/<str:punto>/<str:numero>/', views.abrir_mesa_view, name='abrir_mesa'),
    
    path('comanda/<str:punto>/<str:numero>/<str:folio>/', views.comanda_view, name='comanda'),
]