# MerquenPOS 🍽️

Sistema de Punto de Venta (POS) diseñado para la gestión eficiente de restaurantes y hoteles. Desarrollado con **Django** y optimizado para pantallas táctiles (tablets y teléfonos móviles), permite el control ágil de mesas, comandas, sub-cuentas y despacho automático de pedidos hacia distintas áreas de preparación (cocina, bar, cuarto frío, etc.).

---

## 🚀 Características Principales

* **Control de Mesas en Tiempo Real:** Visualización por puntos de venta (Salón, Terraza, Bar, etc.) con estados diferenciados (*Libre*, *Ocupada*, *Cuenta Impresa*), bloqueo automático de concurrencia por usuario y actualización periódica sin recargar la página.
* **Gestión de Sub-cuentas y Cubiertos:** Creación de múltiples sub-cuentas por mesa, traspaso de productos comandados entre cuentas y teclado numérico táctil para modificar comensales.
* **Menús Configurables (Armables):** Confección dinámica de menús (ej. *Menú Ejecutivo*) divididos por tiempos o agrupaciones (Aperitivos, Entradas, Fondos, Bebidas, Postres, Bajativos) con selectores táctiles (`+`/`-`) y opción de completar menús parcialmente comandados.
* **Despacho Inteligente a Áreas de Preparación:** Enrutamiento automático de pedidos a sus impresoras y tablas de destino (`pcocina`, `pbar`, etc.), asociando el producto padre junto con sus agregados y opciones.
* **Variedades y Notas en Línea:** Selección de puntos de cocción o variedades obligatorias y edición de notas personalizadas por producto (ej. *"Sin mayonesa"*) tanto antes como después de agregar al ticket.
* **Búsqueda Rápida e Interfaz Táctil:** Buscador predictivo en tiempo real por nombre de producto, multiplicador de cantidades y diseño responsivo adaptado a garzones en terreno.
* **Seguridad Reforzada:**
  * Validación de precios y cantidades directamente en el servidor desde la base de datos.
  * Autorización con credenciales de **Supervisor/Administrador** para anulación de productos ya comandados.
  * Protección contra fuerza bruta (rate limiting) en el inicio de sesión e higienización contra XSS.

---

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnología |
| :--- | :--- |
| **Backend** | Python 3.11+, Django 5.2 |
| **Base de Datos** | Microsoft SQL Server (`mssql-django`, `pyodbc`, ODBC Driver 17) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Font Awesome 6.4 |
| **Configuración** | `python-dotenv` para gestión de variables de entorno (`.env`) |

---

## 📂 Estructura del Proyecto

```text
MerquenPOS/
├── MerquenPOS/          # Configuración principal del proyecto Django (settings, urls, auth views)
├── POS/                 # Aplicación principal del Punto de Venta
│   ├── services.py      # Lógica de negocio y consultas SQL Server parametrizadas
│   ├── views.py         # Vistas y endpoints API JSON para mesas, tickets y menús
│   ├── urls.py          # Rutas del módulo POS
│   └── tests.py         # Suite de pruebas unitarias y de seguridad
├── static/              # Recursos estáticos (logos, iconos)
├── templates/           # Plantillas HTML responsivas
│   ├── login.html       # Pantalla de acceso táctil
│   └── POS/
│       ├── mesas.html   # Mapa de mesas por punto de venta
│       └── comanda.html # Toma de pedidos, ticket y modales de menú/notas
├── .env.example         # Plantilla de variables de entorno
├── manage.py            # Utilidad de administración de Django
└── requirements.txt     # Dependencias de Python
```

---

## ⚙️ Requisitos Previos

Asegúrate de contar con lo siguiente en el equipo o servidor donde se ejecutará el sistema:

1. **Python 3.10 o superior**
2. **Microsoft SQL Server** (Express o superior)
3. **ODBC Driver 17 for SQL Server** instalado en el sistema operativo

---

## 💻 Instalación y Configuración Local (Desarrollo)

Sigue estos pasos para levantar el proyecto en tu entorno local:

### 1. Clonar el repositorio

```bash
git clone https://github.com/ceal2013/MerquenPOS.git
cd MerquenPOS
```

### 2. Crear y activar el entorno virtual

```powershell
# Crear el entorno virtual
python -m venv venv

# Activar en Windows (PowerShell / CMD):
.\venv\Scripts\activate

# Activar en macOS / Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno (`.env`)

Crea un archivo llamado `.env` en la raíz del proyecto (al mismo nivel que `manage.py`) copiando la plantilla `.env.example`:

```env
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
DJANGO_SECRET_KEY=dev-key-local-merquenpos

DB_NAME=MerquenDB
DB_USER=sa
DB_PASSWORD=tu_password_sql
DB_HOST=localhost\SQLEXPRESS
```

### 5. Iniciar el servidor de desarrollo

```bash
python manage.py runserver 0.0.0.0:8000
```

> **Tip:** Usar `0.0.0.0:8000` permite acceder a la aplicación desde tablets o teléfonos conectados a la misma red Wi-Fi ingresando `http://<IP-DEL-SERVIDOR>:8000`.

---

## 🧪 Ejecución de Pruebas

El proyecto cuenta con pruebas automatizadas para validar las reglas de seguridad, integridad de precios, autorizaciones y renderizado de plantillas:

```bash
python manage.py test POS
```

---

## 🌐 Pase a Producción (Instalación en Clientes)

Al desplegar el sistema en el servidor de un cliente (hotel o restaurante):

1. **Configura el archivo `.env` de producción:**
   ```env
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=192.168.1.100,merquenpos.local
   DJANGO_CSRF_TRUSTED_ORIGINS=http://192.168.1.100,http://merquenpos.local
   ```
2. **Genera una clave secreta única (`DJANGO_SECRET_KEY`) por cliente:**
   Ejecuta en la terminal del servidor y pega el resultado en `.env`:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

---

## 🔒 Buenas Prácticas de Seguridad

* **Nunca subas el archivo `.env` al repositorio.** Utiliza siempre `.env.example` como referencia.
* El archivo `.gitignore` ya excluye `.env`, `*.log`, `__pycache__/` y `venv/`.
* Mantén `DJANGO_DEBUG=False` en cualquier entorno accesible por red en producción.
