#addons/modulo_prueba/models/task.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError #importa un error especial de odoo, sirve para mostrar mensajes de validación en la interfaz

#(models.Model): significa q este modelo será persistente y tendrá tabla en odoo
class Task(models.Model):
    _name = "modulo_prueba.task" #nombre del módulo. nombre del modelo, odoo lo convierte en la tabla 'modulo_prueba_task'
    _description = "User Task" #es lo q sale en la interfaz de odoo para referirse al modelo, como por ejm en títulos de vistas
    _order = 'deadline asc' #campo q hace q cuando Odoo muestre las tareas las ordenará por deadline de MENOR A MAYOR
 
    name = fields.Char(string = 'Nombre', required= True, help='Introduzca el nombre') #.Char() es un texto corto, help='': genera un tooltip con un string dentro
    description = fields.Text(string='Descripción') #.Text() nos permite meter un texto largo

    creation_date = fields.Date(string = 'Fecha de creación')
    start_date = fields.Datetime(string = 'Fecha de inicio')
    end_date = fields.Datetime(string = 'Fecha de finalización')
    is_paused = fields.Boolean(string = 'Está pausado?')

    """ --------------- CAMPOS RELACIONALES ------------------------
-  TASK.PY ES EL MODELO CENTRAL: Una tarea pertenece a un usuario, esta tarea puede pertenecer a un SPRINT y puede tener varias TECNOLOGÍAS

                res.users
                ^
                | Many2one ---> Un usuario puede tener varias tareas (MANY) y una tarea sólo pertenece (TO) a un usuario (ONE)
                |
                modulo_prueba.task
                |
                | Many2one ---> Un sprint puede tener muchas tareas (MANY) y una tarea pertenece a (TO) un sólo Sprint (ONE)
                \
                  modulo_prueba.sprint

                                  Many2many
                modulo_prueba.task  <-->  modulo_prueba.tecnologia -> Una tarea puede usar muchas (MANY) tecnologías, y (TO) una tecnología puede estar en muchas (MANY) tareas
                                     |
        Many2many mediante tabla intermedia: modulo_prueba_task_tecnologia_rel


===================== EXPLICACIÓN DE LAS 3 RELACIONES =====================
Many2one: - Muchos -> Uno (N:1)
          - Equivalente SQL: FOREIGNKEY         <-----------------------------------
          - Una tarea tiene un sprint
          - Se guarda una columna sprint_id en la tabla task
          - Se ve como desplegable

One2many: - Uno -> Muchos (1:N)
          - Equivalente SQL: Inversa de FOREIGNKEY      <---------------------------
          - Un sprint muestra muchas tareas
          - No crea columna nueva
          - Usa el campo sprint_id de Task para buscar

Many2many: - Muchos <--> Muchos (N:N)
           - SE GENERA TABLA INTERMEDIA         <------------------------------------
           - Una tarea tiene muchas tecnologías y una tecnología muchas tareas
           - Usa tabla intermedia
           - Se puede ver como tags, checkboxes, lista, etc
           - Esta relación no se guarda como una columna, se guarda como una tabla aparte, el nombre se asigna automáticamente pero lo podemos poner con relation=''

                            modulo_prueba_task_tecnologia_rel
                            ----------------------------------
                                task_id    |  tecnologia_id
                            ---------------|------------------
                                    1      |        3
                                    1      |        4
                                    2      |        3
============================================================================


- Many2one: Por convención sus campos suelen terminaer en '_id'
- .One2many(): Relación inversa del Many2one
- One2many/Many2many: Se manipulan internamente con comandos especiales cuando se escriben desde código
- Many2many: Igual q en las BBDD, las relaciones de muchos-a-muchos van a crear tablas intermedias con los 'ids' de ambas tablas relacionadas


    'user_id' es el campo de relación, osea cada tarea (del modelo task) va a tener un usuario asignado y su id se va a guardar en ese campo
    'user_id' es'Many2one' lo q quiere decir que un usuario puede tener muchas tareas asignadas, pero cada tarea es asignada a 1 solo usuario 
    'self.env.user' -> entorno vistual de odoo, con .user accede al usuario actual logeado, con 'default=lambda self:self.env.user' me dice que por default asigne la tarea al usuario conectado ahora mismo
    required=True obliga a asignar una persona
    'comodel_name' sirve para indicar el nombre del modelo destino con el que se va a relacionar este campo, basicamente pa q postgre pueda hacer la 'FOREIGN KEY' 
     'res.users' es un modelo q ya existe en odoo y contiene usuarios y hay más como:
                    res.partner      ->  contactos/clientes/proveedores
                    product.product  -> productos
                    product.template -> plantillas de producto
                    stock.picking    -> albaranes
                    stock.move       -> movimientos de inventario
                    sale.order       -> pedidos de venta
                    purchase.order   -> pedidos de compra
                    account.move     -> facturas
                    hr.employee      -> empleados
                    ir.rule          -> reglas (se usa luego en task_securiy.xml)                                                                                  """

    # (many) TAREA -> USUARIO (one)
    user_id = fields.Many2one( 
        comodel_name='res.users', #comodel_name: modelo con el q se conecta el campo 
        string='Asignado a', # texto visible en la interfaz
        default=lambda self:self.env.user, #explicado en línea 45
        required= True #obliga al usuario a llenarlo
    )
    
    # (many) TAREA -> SPRINT (one)
    sprint_id = fields.Many2one(
        comodel_name='modulo_prueba.sprint', #el destino del campo es el modelo sprint
        string='Sprint',
        ondelete='set null', # Si se borra el print, las tareas no se borran, solo se quedan en NULL
        help='Sprint relacionado' #tooltip
    )

    # (many) TAREA <--> TECNOLOGIAS (many)
    tecnologias_ids = fields.Many2many(
        comodel_name='modulo_prueba.tecnologia', #modelo destino con el q se va a enlazar
        relation='modulo_prueba_task_modulo_prueba_tecnologia_rel', #nombre de la tabla intermedia q se va a crear, la convención para el nombre es 'nombreModulo_
        column1='task_id', #columna que apunta a la tarea
        column2='tecnologia_id', #columna q apunta a tecnologia
        string='Tecnologías' #texto visible
    )


    priority = fields.Selection( #crea un desplegable de seleccion donde Odoo guarda 1 pero el usuario ve 'Media', etc
        [('0','Baja'),('1','Media'),('2','Alta')],
        string='Prioridad',
        default= '1',
    )
    #campo desplegable tmb de tipo selection, se recomienda siempre usar 'state' como nombre para los campos de estados, en otros podemos ponerle el nombre q queramos (exepto a 'name')
    state = fields.Selection(
        [('draft','Borrador'),('in_progress','En Progreso'),('done','Completada')],
        string='Estado',
        default= 'draft',
    ) 
    deadline = fields.Date(string='Fecha Límite') #campo tipo fecha 
    is_done = fields.Boolean(string='Completada', compute= '_compute_is_done', store=True) #campo booleano calculado donde compute= '_compute_is_done' dice q el valor se calcula con el '_compute_is_done', store=True hace q el valor se guarde en postgre

    ''' api : Módulo de odoo, importado arriba y tiene varios decoradores como @api y son usados para desarrollar módulos:
                    - @api.depends(): Recalcula campos COMPUTE que dependan de otros en cuanto se produzca un cambio en el estado de dicho campo
                    - @api.constrains(): Valida datos, básicamente pone restricciones, si se cumple la validación definida te deja ejecutar el código, si no, te muestra un ValidationError
                    - @api.onchange(): Cuando el usuario modifica un campo en el formulario, este actualiza la vista de la interfaz pero sin guardar los cambios
                    - @api.model(): Indica que un método trabaja con el modelo, no con registros concretos, usado con create(), búsquedas y utilidades
                    - @api.model_create_multi(): 
                    - @api.autovacuum(): 
                    - @api.private()


    '''
    @api.depends('state') #hace q cuando cambie STATE se debe recalcular este campo
    def _compute_is_done(self):
        for record in self: #self puede contener varios registros y por eso debe recorrerse
            record.is_done = record.state == 'done' #si esl estado es 'done, 'is_done' será TRUE pero si no, será FALSE

    """ PYTHON CONSTRAINTS: Sirven para evitar que los usuarios ingresen datos incorrectos (prevenir campos vacios, q se repitan valores o campos donde solo deben ir numeros o letras)     
    @api.constrains('campo1', 'campo2'): Decorado donde en '()' se definen los campos donde se va a ver aplicada la restricción. SÓLO ADMITE NOMBRE DE CAMPOS SIMPLES (sin '_', '.')
    ValidationError(): Es la excepción que siempre se espera en un constrains en caso de q la validación falle, viende de la libreria exeptions de Odoo
    'def _check_deadline(self):': Siempre se debe de declarar un método vacío y dentro de ella la validación (for task in...)
    """
    @api.constrains("deadline") #le dice a Odoo q esta función validará el campo deadline
    #valida q la fecha límite no sea anterior a hoy
    def _check_deadline(self):
        for task in self: #recorre las tareas q se están guardando
            if task.deadline and task.deadline < fields.Date.today(): # 'si hay fecha límite y es menor que hoy, hay error'
                #se lanzará un error si alguien intenta guardar una tarea con una fecha vencida
                raise ValidationError('La fecha límite no puede ser anterior a hoy')


