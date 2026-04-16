from django.contrib import admin
from django.urls import path, include
from MerquenPOS import views as global_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta principal para la pantalla de inicio de sesión
    path('', global_views.login_global_view, name='login'),
    
    # Ruta para ejecutar la función de cierre de sesión
    path('logout/', global_views.logout_global, name='logout'),
    
    # Inclusión de las rutas específicas del módulo de mesas y pedidos
    path('pos/', include('POS.urls')),
]