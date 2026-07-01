#addons/modulo_prueba/models/task.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError #importa un error especial de odoo, sirve para mostrar mensajes de validación en la interfaz
from datetime import timedelta

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
        column1='modulo_prueba_task_id', #columna que apunta a la tarea
        column2='modulo_prueba_tecnologia_id', #columna q apunta a tecnologia
        string='Tecnologías' #texto visible
    )

    priority = fields.Selection( #crea un desplegable de seleccion donde Odoo guarda 1 pero el usuario ve 'Media', etc
        [('0','Baja'),('1','Media'),('2','Alta')],
        string='Prioridad',
        default= lambda self: self._get_default_priority(), #la prioridad por defecto viene del método '_get_defaul_priority', así no está hardcoreada y sale dew un método reutilizable,
    )
    #campo desplegable tmb de tipo selection, se recomienda siempre usar 'state' como nombre para los campos de estados, en otros podemos ponerle el nombre q queramos (exepto a 'name')
    state = fields.Selection(
        [('draft','Borrador'),('in_progress','En Progreso'),('done','Completada')],
        string='Estado',
        default= 'draft'
    ) 
    deadline = fields.Date(string='Fecha Límite') #campo tipo fecha 
    is_done = fields.Boolean(string='Completada', compute= '_compute_is_done', store=True) #campo booleano calculado donde compute= '_compute_is_done' dice q el valor se calcula con el método del mismo nombre

    days_remaining = fields.Integer(                # 2DO CAMPO CALCULADO: - 'days_remaining' no se escribe manualmente
        string='Días restantes',                    #                      - Odoo lo calcula usando el método '_compute_days_remaining'
        compute='_compute_days_remaining',          #                      - 'store=True' hace que el resultado se guarde en PostgreSQL
#store=True hace q el valor se guarde en postgre    #                      - @api.depends('deadline') indica que debe recalcularse cuando cambie deadline
        store=True                                  
    )

    context_info = fields.Char(   #campo calculado que cambia según el contexto de Odoo
    #no ponemos 'store=True' pq el contexto puede variar según el usuario, idioma o empresa y si lo guardamos en la bbdd este valor se vuelve fijo
        string='Info Contexto',
        compute='_compute_context_info'
    )                                          

    ''' api : Módulo de odoo, importado arriba y tiene varios decoradores como @api, etc. Se usan para definir el comportamiento a los métodos, controlar el flujo de datos o gestionar la BBDD:
    Documentación oficial de Odoo19 los define como decoradores de método del ORM
    Aquí algunos ejemplos:  * @api.model para métodos de modelo
                            * @api.ondelete para lógica durante unlink()
                            * @api.depends_context para campos calculados dependientes del contexto
                            * @api.private para evitar llamadas RPC
                            * @api.autovacuum para tareas llamadas por el cron diario ir.autovacuum

            - @api.depends('campo_a', 'campo_b'): 
                    Obligatorio para campos calculados (compute). 
                    Escucha los cambios en los campos indicados como argumentos y recalcula el valor del campo compute en tiempo real tanto en la interfaz como al guardar en la base de datos.

            - @api.depends_context('clave_contexto_a', 'clave_contexto_b'):
                Se usa en campos calculados que NO solo dependen de campos del registro, sino también del contexto de ejecución de Odoo.
                El "context" es información extra que Odoo pasa internamente, como la compañía activa, el idioma, el usuario, la fecha, permisos, etc.
                Si cambia alguno de los valores del contexto indicados, Odoo sabe que debe recalcular el campo compute.
                * Ejemplo:
                    @api.depends_context('company')   ->      En ese caso, el cálculo puede variar según la compañía activa.
                    def _compute_price(self):                 No se usa para campos normales del modelo, sino para valores del contexto. 
                        ...

            - @api.ondelete(at_uninstall=False): Se usa para definir validaciones o bloqueos cuando se intenta eliminar un registro con unlink()
                    Sirve para evitar que los registros sean borrados si no cumplen una condición
                    A diferencia de sobreescribir directamente unlink(), api.ondelete está pensado para que las validaciones de borrado no bloqueen la desinstalación del módulo.
                    Por defecto es 'at_uninstall=False', osea la validación NO se ejecuta cuando Odoo está desinstalando el módulo
                    * Ejemplo:
                                @api.ondelete(at_uninstall=False).      -> Aquí Odoo impediría borrar tareas que no estén completadas, 
                                def _unlink_if_not_done(self):             pero permitiría limpiar datos durante la desinstalación del módulo
                                    for record in self:
                                        if record.state != 'done':
                                            raise UserError("Solo puedes borrar tareas completadas.")

            - @api.constrains('campo_a'): 
                    Establece restricciones de validación a nivel de servidor del backend. 
                    Si los datos ingresados por el usuario violan la lógica programada, interrumpe la ejecución del código y lanza un aviso en pantalla mediante 
                    un "ValidationError", haciendo q no se guarden datos incorrectos.

            - @api.onchange('campo_a'): 
                    Se activa desde el formulario cuando el usuario modifica un campo
                    Cuando el usuario modifica el valor de un campo dentro de un formulario, actualiza de forma visual otros campos de la pantalla al instante, 
                    pero SIN guardar los cambios en la base de datos hasta que el usuario pulse el botón manual de guardar.

            - @api.model: 
                    Indica que el método actúa a nivel de modelo y no sobre un registro (record) con un ID específico
                    self sigue siendo un recordset de Odoo, pero no necesitamos que contenga una tarea específica
                    Se usa habitualmente en métodos de utilidad genéricos y en búsquedas personalizadas

            - @api.model_create_multi: 
                    El estándar moderno y obligatorio en Odoo 19 para la creación de registros. 
                    Fuerza a que el método "create()" reciba una lista de diccionarios (vals_list), lo q permite al ORM realizar 
                    inserciones de datos masivas (Bulk Inserts) en una única transacción de PostgreSQL para optimizar el rendimiento del servidor.

            - @api.autovacuum: 
                    Decorador especial para automatizaciones del sistema. 
                    Indica al framework que el método decorado debe ejecutarse de forma automática y periódica por el motor 
                    interno de Odoo para realizar tareas rutinarias de limpieza (como eliminar adjuntos huérfanos, vaciar sesiones web caducadas o purgar registros temporales).

            - @api.private: 
                    Convierte el método en una función privada del sistema. 
                    Bloquea de forma estricta que el método pueda ser invocado o llamado de forma remota desde fuera del servidor 
                    a través de protocolos API o llamadas externas como RPC, protegiendo funciones críticas o sensibles de lógica interna.                                          '''

    @api.depends('state') #hace q cuando cambie STATE se debe recalcular este campo
    #CONVENCIÓN DE NOMBRE PARA MÉTODOS DE @api.depends(): el nombre de la función debe comenzar por '_' (indica que es privado) 
    # seguido de la palabra 'compute' seguido del nombre del campo
    def _compute_is_done(self): 
        for record in self: #self puede contener varios registros y por eso debe recorrerse
            record.is_done = record.state == 'done' #si esl estado es 'done, 'is_done' será TRUE pero si no, será FALSE

    @api.depends('deadline')
    def _compute_days_remaining(self):
        today= fields.Date.today() #Variable que guarda la fecha de hoy
        for task in self:
            if task.deadline: #si la tarea tiene fecha límite asignada
                task.days_remaining = (task.deadline - today).days #me calcula los días restantes restando la fecha límite con la fecha actual
            else:
                task.days_remaining = 0 #si no se cumple el caso de arriba entonces muestra 0

    """ PYTHON CONSTRAINTS: Sirven para evitar que los usuarios ingresen datos incorrectos (prevenir campos vacios, q se repitan valores o campos donde solo deben ir numeros o letras)     
        @api.constrains('campo1', 'campo2'): Decorado donde en '()' se definen los campos donde se va a ver aplicada la restricción. SÓLO ADMITE NOMBRE DE CAMPOS SIMPLES (sin '_', '.')
        ValidationError(): Es la excepción que siempre se espera en un constrains en caso de q la validación falle, viende de la libreria exeptions de Odoo
        'def _check_deadline(self):': Siempre se debe de declarar un método vacío y dentro de ella la validación (for task in...)
        """
    @api.constrains("deadline") #le dice a Odoo q esta función validará el campo deadline
    #la convención para ponerle nombre a las validaciones de datos es _check_ seguido del nombre del campo que estás comprobando
    def _check_deadline(self):#valida q la fecha límite no sea anterior a hoy
        for task in self: #recorre las tareas q se están guardando
            if task.deadline and task.deadline < fields.Date.today(): # 'si hay fecha límite y es menor que hoy, hay error'
                #se lanzará un error si alguien intenta guardar una tarea con una fecha vencida
                raise ValidationError('La fecha límite no puede ser anterior a hoy')

    @api.constrains('start_date', 'end_date') 
    def _check_dates (self):                                              # Se ejecuta en create/write cuando se modifican start_date o end_date
        for task in self:                                                 # Impide guardar una tarea con fecha de fin anterior a fecha de inicio
            if task.start_date and task.end_date and task.end_date < task.start_date:
                raise ValidationError('La fecha de finalización no puede ser anterior a la fecha de inicio')

    #Cuando ponga como prioridad 'Alta', Odoo debe cambiar 'Estado' para que esté en 'En Progreso' antes de haber presionado el botón guardar
    @api.onchange('priority')
    #para '@api.onchange' se debe empezar el nombre con '_onchange_' + el nombre del campo como buena práctica
    def _onchange_priority(self):
        if self.priority == '2' and self.state == 'draft':
            self.state = 'in_progress'

    @api.model_create_multi
    def create(self, vals_list):
        today = fields.Date.today()
        for vals in vals_list:
            if not vals.get('creation_date'):
                vals['creation_date'] = today
        return super().create(vals_list)

    @api.model
    #PARA PROBARLO: Cambiamos el default de priority en el método, actualizamos y comprobamos que cambió el default en el formulario
    #método a nivel de modelo, no necesitan haber tareas para que Odoo tenga esta lógica porque actua sobre el modelo, no sobre cada 'record'
    def _get_default_priority(self): #devuelve la prioridad por defecto que pondrá Odoo cuando creemos tareas
        return '1'

    @api.ondelete(at_uninstall=False)
    #PARA PROBARLO: Intentar borrar una tarea draft -> debe bloquear
    #               Cambia la tarea a done y bórrala -> debe permitir
    def _unlink_except_done(self):
        #Se ejecuta cuando alguien intenta borrar registros con unlink()
        #'at_uninstall=False': Significa que esta validación NO se ejecutará cuando Odoo esté desinstalando el módulo, para evitar dejar la base de datos a medias                          
        for task in self:
            if task.state != 'done':
                raise UserError('Solo puedes eliminar tareas completadas.')

    @api.depends_context('uid', 'company', 'lang')
    def _compute_context_info(self):
        """ @api.depends_context: Se usa cuando el campo calculado depende del contexto de Odoo, no sólo de campos del registro
                                        uid     -> usuario actual
                                        company -> compañía actual
                                        lang    -> idioma activo en el contexto                      
        En este caso lo q pasa es q cuando odoo muestra el formulario calcula 'context_info' sacando la info del env
        pero el contenido puede variar según usuario, empresa o idioma, por lo q si otro usuario abre la misma tarea este podría ver otro texto  """        
        lang = self.env.context.get('lang') or 'sin idioma'
        user = self.env.user.name # '.env': Entorno, es el objeto central de odoo que almacena tdoo el contexto de la sesión actual
        company = self.env.company.name

        for task in self:
            #'f': Son 'f-strings' y se usan para inyectar variables directamente dentro de una cadena de texto 
            #     sin tener que cerrar cada texto en comillas y concatenar con '+' como se suele hacer
            task.context_info = f'Usuario: {user} | Empresa: {company} | Idioma: {lang}'

#SI ES UN MÉTODO AUXILIAR INTERNO DEBE SER PRIVADO - método interno de apoyo
    #método para crear una descripción por default, va a ir conectado a un botón en 'task_views.xml'
    @api.private  # Marca este método como interno y hace que no pueda llamarse desde una RPC/API externa
    def _build_default_description(self): #por convención, su nombre empieza por '_' para indicar que es un método privado
        #Este método sólo prepara un texto; no escribe directamente en base de datos        
        self.ensure_one()
        #'f': Son 'f-strings' y se usan para inyectar variables directamente dentro de una cadena de texto 
        #     sin tener que cerrar cada texto en comillas y concatenar con '+' como se suele hacer
        return f'Tarea "{self.name}" asignada a {self.user_id.name}'

#SI UN MÉTODO ESTÁ PENSADO PARA SER BOTÓN O API PUEDE SER PÚBLICO - método q el usuario puede ejecutar
    def action_fill_description(self): #Método público llamado desde un botón de la vista
                                       #usa internamente el método privado _build_default_description()
        for task in self:
            task.description = task._build_default_description()

    ''' Una vez al día, Odoo ejecuta el cron de autovacuum, el cual busca métodos marcados con: @api.autovacuum y los ejecuta'''
    @api.autovacuum #Método llamado automáticamente por el cron diario de limpieza de Odoo
    def _gc_old_done_tasks(self): #Método programado para que borre las tareas completadas con fecha de creación anterior a 30 días
                                  #Además sólo borra tareas en estado done para no chocar con @api.ondelete
        limit_date = fields.Date.today() - timedelta(days=30)
        old_done_tasks = self.search([
            ('state', '=', 'done'),
            ('creation_date', '<', limit_date),
        ])
        count = len(old_done_tasks)
        old_done_tasks.unlink()
        return count, 0

        ''' 1. Añade @api.model y cambia default de priority
            2. Actualiza módulo
            3. Crea una tarea nueva y comprueba que priority sale en Media

            4. Añade @api.ondelete
            5. Intenta borrar una tarea draft: debe bloquear
            6. Cambia la tarea a done y bórrala: debe permitir

            7. Añade @api.depends_context + context_info
            8. Muéstralo en la vista
            9. Abre una tarea y comprueba el texto

            10. Añade @api.private + botón action_fill_description
            11. Pulsa el botón y comprueba que rellena description

            12. Añade @api.autovacuum
            13. Déjalo como ejercicio de limpieza automática; no hace falta forzarlo todavía'''