#addons/modulo_prueba/models/students.py
from odoo import models, fields #importaciones

'''los modelos se crean heredando a:
  - Model: Modelos regulares persistentes, cada regustro q guardemos ahí se va a quedar almacenado en la BD
  - TransientModel: Datos temporales q se almacenan en la BD y se borran automaticamente de vez en cuando
  - AbstractModel: No tienen tablas de la BD vinculadas a ella y pueden ser compartidas por múltiples modelos heredados'''
class Student(models.Model):
    _name = 'modulo_prueba.student' #nombre del módulo. nombre del modelo, sirve para colocarlo en el XML de la vista 
    _description = 'Tabla de estudiantes' 

#los campos se definen con fields y son atributos de la clase del modelo, definen que puede alamcenar el modelo y dónde:
    name = fields.Char(string='Nombre', required= True) #crea la tabla/modelo de datos, en el templates.xml se pone:  <field name="model">modulo_prueba.student</field>
    age = fields.Integer(string='Edad')

#un MODELO en odoo, se refleja en la BBDD como una TABLA, CADA MODELO ES UNA TABLA