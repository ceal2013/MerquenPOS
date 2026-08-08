# MerquenPOS 🍽️

Sistema de Punto de Venta (POS) diseñado para la gestión eficiente de restaurantes y hoteles. Desarrollado con Django y optimizado para pantallas táctiles (tablets y celulares), permite el control rápido de comandas, mesas y pedidos dirigidos a distintas áreas de preparación (cocina, bar, cuarto frío, etc.).

---

## 🚀 Características Principales

* **Control de Mesas y Sub-cuentas:** Gestión visual de mesas, manejo de sub-cuentas por mesa y modificación de cubiertos.
* **Menús Configurables:** Confección dinámica de menús (ej. Menú Ejecutivo) divididos por agrupaciones (Aperitivos, Entradas, Fondos, Bebidas, Postres, Bajativos) con selectores de cantidad táctiles (+/-).
* **Despacho Inteligente a Destino:** Enrutamiento de pedidos a sus impresoras/tablas de destino (`pcocina`, `pbar`, etc.), enviando el producto padre como cabecera junto a sus productos opciones.
* **Gestión de Variedades y Notas:** Registro de puntos de cocción o adiciones personalizadas ("Sin mayonesa") por producto.
* **Búsqueda Rápida e Interfaz Táctil:** Buscador predictivo en tiempo real por nombre de producto y diseño responsivo optimizado para garzones.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.x, Django 5.x
* **Base de Datos:** Microsoft SQL Server (vía `mssql-django` y ODBC Driver)
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5, FontAwesome
* **Seguridad:** `python-dotenv` para manejo seguro de variables de entorno

---

## ⚙️ Requisitos Previos

Asegúrate de contar con lo siguiente en el equipo donde se ejecutará el sistema:
1. **Python 3.10+**
2. **Microsoft SQL Server** (Express o superior)
3. **ODBC Driver 17 for SQL Server** (o superior)

---

## 💻 Instalación y Configuración Local (Desarrollo)

Sigue estos pasos para levantar el proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/merquenpos.git](https://github.com/tu-usuario/merquenpos.git)
   cd merquenpos
2.	Crear y activar el entorno virtual:
python -m venv venv

# En Windows (PowerShell / CMD):
venv\Scripts\activate

# En macOS / Linux:
source venv/bin/activate
3.	Instalar dependencias:
pip install -r requirements.txt
4.	Crear el archivo .env: Crea un archivo llamado exactamente .env en la raíz del proyecto (al mismo nivel que manage.py) basándote en la plantilla .env.example:
Fragmento de código
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DJANGO_SECRET_KEY=dev-key-local-merquenpos

DB_NAME=MerquenDB
DB_USER=sa
DB_PASSWORD=tu_password_sql
DB_HOST=localhost\SQLEXPRESS
5.	Iniciar el servidor de desarrollo:
python manage.py runserver 0.0.0.0:8000
El parámetro 0.0.0.0:8000 permite acceder a la aplicación desde tablets o teléfonos conectados a la misma red local.
🌐 Pase a Producción (Instalación en Clientes)
Cada vez que instales el sistema en un nuevo servidor de producción:
1.	Modifica el archivo .env del servidor con los siguientes parámetros:
Fragmento de código
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=192.168.1.100,merquenpos.local
2.	Generar una nueva clave secreta (DJANGO_SECRET_KEY): Ejecuta el siguiente comando en la terminal del servidor para obtener una clave única de 50 caracteres y pégala en el .env:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
🔒 Seguridad
•	Jamás subas el archivo .env a GitHub.
•	El archivo .gitignore debe incluir las entradas .env, *.log, __pycache__/ y la carpeta venv/.

