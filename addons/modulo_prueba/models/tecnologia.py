#addons/modulo_prueba/models/tecnologia.py
from odoo import models, fields
class Tecnologia(models.Model):
    _name = "modulo_prueba.tecnologia" #nombre del módulo. nombre del modelo, odoo lo convierte en la tabla 'modulo_prueba_tecnologia'
    _description = "Tecnología" #es lo q sale en la interfaz de odoo para referirse al modelo, como por ejm en títulos de vistas

    name = fields.Char(string = 'Nombre') #.Char() es un texto corto, help='': genera un tooltip con un string dentro
    description = fields.Text(string='Descripción') #.Text() nos permite meter un texto largo
    photo = fields.Image(max_width=200, max_height=200)

    '''
    - 2do 'Many2many', el 1ero está en 'task.py' y este es el inverso de ese
    - relation='': nombre de la tabla intermedia que usa Odoo para guardar la relación Many2many, la convención para ponerle nombre es 'nombreModeloActual_nombreModeloDestino_rel'
    (many) TECNOLOGIAS <--> TAREA (many)                                '''
    task_ids = fields.Many2many(
        comodel_name='modulo_prueba.task',  
        relation='modulo_prueba_task_modulo_prueba_tecnologia_rel', #usa la misma tabla intermedia q el many2many de task.py
        column1='modulo_prueba_tecnologia_id', #invierte el orden de las columnas, ahora se apunta primero a tecnologia_id
        column2='modulo_prueba_task_id', #y luego a task_id
        string='Tareas'
        #T.ODO ESTO PERMITE QUE UNA TECNOLOGIA PUEDA VER SUS TAREAS RELACIONADAS
    )