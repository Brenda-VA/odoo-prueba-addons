# addons/modulo_prueba/__init__.py
# init nos indica donde se encuentran los archivos python de nuestro proyecto (pero desde la carpeta raíz)
from . import controllers 
from . import models

'''             Arqiuitectura similar a MVC
       ------- XML -------     --------- .PY --------- 
        VISTA (Interfaz)              MODELO
        - Campos                - Estructura de datos
        - Botones                   CONTROLADOR
        - Pantallas, etc        - Lógica de negocio                     
        
       '''
