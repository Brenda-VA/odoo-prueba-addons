# addons/modulo_prueba/models/sprint.py
from odoo import models, fields
class Sprint(models.Model):
    _name = "modulo_prueba.sprint" #nombre del módulo. nombre del modelo, odoo lo convierte en la tabla 'modulo_prueba_sprint'
    _description = "Sprint" #es lo q sale en la interfaz de odoo para referirse al modelo, como por ejm en títulos de vistas

    name = fields.Char(string = 'Nombre') #.Char() es un texto corto, help='': genera un tooltip con un string dentro
    description = fields.Text(string='Descripción') #.Text() nos permite meter un texto largo
    start_date = fields.Datetime(string = 'Fecha de inicio')
    end_date = fields.Datetime(string = 'Fecha de finalización')

    """ CAMPO One2many: Relación inversa del Many2one    
    NO PUEDE EXISTIR SÓLO, NECESITA UN Many2one DEL CUAL BUSCAR DATOS
    task_ids: Nombre del campo, por convención debe terminar en _ids
    Esto no crea una columna nueva en la tabla 'modulo_prueba_sprint', si no q busca tareas cuyo 'sprint_id' sea el sprint actual:
    Por ejemplo: 
    -> Sprint A tiene 'id = 5' ---> Odoo busca: 'modulo_prueba.task' donde 'sprint_id = 5'    
    
    Entonces si encuentra:  Tarea 1 -> sprint_id = 5
                            Tarea 2 -> sprint_id = 5
                            Tarea 7 -> sprint_id = 5                                                                     
                            
    Me muesta en el formylario de sprint todas esas tareas en 'task_ids'
    -> Por eso 'One2many' es el inverso de 'Many2one

                           
    SPRINT (one) --> TAREAS (many)                                                                 """
    task_ids = fields.One2many( # q sea One2many significa q este campo contiene una colección de registros hijos, se muestran en forma de tabla con 'add a line'
        comodel_name='modulo_prueba.task', # apunta al modelo destino
        inverse_name='sprint_id', # como FK, apunta al campo 'Many2one' que está en 'task.py', debe ser el inverso
        string='Tareas'
    )