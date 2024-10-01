## Project Structure

The project follows the following directory structure:

```
sar-flask/
    ├── templates/                  # Plantillas HTML
    │   ├── dual_base.html           # Plantilla base para vistas duales
    │   ├── single_base.html         # Plantilla base para vistas individuales
    │   ├── theater/                 # Plantillas relacionadas con "theater"
    │   │   ├── config_theater.html      # Configuración de "theater"
    │   │   ├── form_edit_theater.html   # Formulario de edición de "theater"
    │   │   ├── form_theater.html        # Formulario de creación de "theater"
    │   │   ├── home.html                # Página principal
    │   │   └── theater_table.html       # Tabla de "theater"
    │   │   
    │   ├── theater_areas/           # Plantillas relacionadas con "theater areas"
    │   │   ├── form_edit_theater_areas.html  # Formulario de edición de "theater areas"
    │   │   └── theater_areas_table.html      # Tabla de "theater areas"
    │   │  
    │   └── theater_versions/        # Plantillas relacionadas con "theater versions"
    │       ├── config_theater_versions.html   # Configuración de "theater versions"
    │       ├── create_theater_versions.html   # Creación de versiones de "theater"
    │       ├── form_edit_theater_version.html # Formulario de edición de versiones de "theater"
    │       └── theater_versions_table.html    # Tabla de versiones de "theater"
    │       
    ├── static/                      # Archivos estáticos (CSS, JS, imágenes)
    │   ├── css/                     # Estilos CSS
    │   │   ├── components/          # Estilos específicos para componentes reutilizables
    │   │   ├── layout/              # Estilos de diseño y maquetación
    │   │   └── utils/               # Estilos de utilidades y funciones auxiliares
    │   │
    │   ├── js/                      # Archivos JavaScript
    │   ├── img/                     # Imágenes
    │   └── ...                      # Otros archivos estáticos
    │   
    ├── db/                          # Archivos relacionados con la base de datos
    │   ├── db_config.py             # Credenciales para acceder a la base de datos
    │   └── db_service.py            # Funciones base para interactuar con la base de datos
    │  
    ├── db_queries.py                # Funciones y procedimientos para modificar información en la base de datos
    ├── routes.py                    # Definición de las rutas de la aplicación
    ├── README.md                    # Archivo de documentación del proyecto
    ├── utils.py                     # Funciones adicionales de utilidad
    └── app.py                       # Punto de entrada de la aplicación
```

