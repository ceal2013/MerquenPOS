MerquenPOS 🍽️

Sistema de Punto de Venta (POS) diseñado para la gestión eficiente de restaurantes y hoteles. Desarrollado con Django y optimizado para pantallas táctiles (tablets/móviles), permite el control rápido de comandas, mesas y pedidos a cocina/bar.

🚀 Características Principales

•	Control de Mesas: Gestión visual de mesas, sub-cuentas y cantidad de cubiertos.

•	Menús Configurables: Sistema dinámico para armar menús (ej. Menú Ejecutivo) con opciones separadas por categorías (Aperitivos, Entradas, Fondos, Bebidas, etc.) y selectores de cantidad táctiles.

•	Comandas a Destino: Enrutamiento inteligente de productos a distintas impresoras o áreas de preparación (Cocina, Bar, Cuarto Frío), incluyendo la agrupación automática de menús (productos padre/hijo).

•	Gestión de Variedades y Notas: Selección rápida de puntos de cocción o adiciones personalizadas ("Sin mayonesa").

•	Interfaz Táctil y Búsqueda: Frontend responsivo usando Bootstrap y JavaScript nativo, con buscador predictivo en tiempo real pensado para el ritmo rápido de los garzones.

🛠️ Tecnologías Usadas

•	Backend: Python 3.x, Django 5.x

•	Base de Datos: Microsoft SQL Server (vía mssql-django y ODBC Driver)

•	Frontend: HTML5, CSS3, JavaScript Vanilla, Bootstrap 5, FontAwesome.

⚙️ Requisitos Previos

Antes de instalar, asegúrate de tener instalado en tu máquina:

1.	Python 3.x
2.	Microsoft SQL Server (Express o superior).
3.	ODBC Driver 17 (o superior) for SQL Server.

💻 Instalación y Configuración Local

Sigue estos pasos para levantar el entorno de desarrollo:

1.	Clonar el repositorio:
Bash
git clone https://github.com/tu-usuario/merquenpos.git
cd merquenpos

2.	Crear y activar el entorno virtual:
Bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

3.	Instalar dependencias:
Bash
pip install -r requirements.txt

4.	Configurar Variables de Entorno: Crea un archivo llamado exactamente .env en la raíz del proyecto (al mismo nivel que manage.py) y agrega tus credenciales locales:
Fragmento de código
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DJANGO_SECRET_KEY=clave-secreta-desarrollo-merquenpos
DB_NAME=MerquenDB
DB_USER=sa
DB_PASSWORD=tu_password_sql
DB_HOST=localhost\SQLEXPRESS

5.	Ejecutar el servidor de desarrollo:
Bash
python manage.py runserver 0.0.0.0:8000
Nota: Se levanta en 0.0.0.0:8000 para poder acceder al sistema desde las tablets o celulares conectados a la misma red local.

🔒 Seguridad
Este proyecto utiliza python-dotenv para proteger las credenciales. Nunca subas el archivo .env al repositorio. Asegúrate de que .env esté siempre incluido en tu archivo .gitignore