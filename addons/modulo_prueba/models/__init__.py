from . import students
from . import task
from . import sprint
from . import tecnologia

''' addons/modulo_prueba/models/__init__.py
los MODELOS son objetos de negocio como Clientes, proveedores, productos, etc
Son declarados como clases python, contienen una lista de atributos y tmb pueden definir su propia lógica de negocio:
  .py -> modelo odoo -> nombre Clase python
                        - campos
                        - funciones                
                        
Odoo cuenta con un ORM (como en Django), el cual traduce el código python a sentencias SQL
Por ejemplo, nuestros modelos se pueden convertir en tablas con solo escribir los campos, los cuales serian cada cada columna de una tabla                         
                    
.py -> modelo odoo -> nombre Clase python -> ORM -> BBDD -> nombre tabla
                        - campos                            campo 1, campo 2
                        - funciones                                                                 '''
