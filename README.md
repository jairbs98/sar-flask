## Project Structure

The project follows the following directory structure:

```
svg_generator/
│
└── app/
    ├── templates/              
    │   ├── dual_base.html           
    │   ├── single_base.html           
    │   ├── theater/           
    │   │   ├── config_theater.html      
    │   │   ├── form_edit_theater.html      
    │   │   ├── form_theater.html      
    │   │   ├── home.html        
    │   │   └── theater_table.html
    │   │   
    │   ├── theater_areas/      
    │   │   ├── form_edit_theater_areas.html     
    │   │   └── theater_areas_table.html      
    │   │  
    │   └── theater_versions/         
    │       ├── config_theater_versions.html     
    │       ├── create_theater_versions.html   
    │       ├── form_edit_theater_version.html  
    │       └── theater_versions_table.html
    │       
    ├── static/                   # Archivos estáticos (CSS, JS, imágenes)
    │   ├── css/
    │   │   ├── components/       # Estilos específicos para componentes reutilizables
    │   │   ├── layout/           # Estilos de diseño y maquetación
    │   │   └── utils/            # Estilos de utilidades y funciones auxiliares
    │   │
    │   ├── js/
    │   ├── img/
    │   └── ...
    │   
    ├── db/
    │   ├── db_config.py          # Credenciales para acceder a la base de datos
    │   └── db_service.py         # Funciones base interactuar con la base de datos
    │  
    ├── db_queries.py             # Funciones y procedimientos para modificar información en base de datos
    ├── routes.py                 # Rutas de la aplicación
    ├── README.md     
    ├── utils.py                  # Funciones adicionales
    └── app.py                    # Punto de entrada de la aplicación

```

