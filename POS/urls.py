from django.urls import path
from . import views

urlpatterns = [
    path('mesas/', views.seleccion_mesas_view, name='seleccion_mesas'),
]