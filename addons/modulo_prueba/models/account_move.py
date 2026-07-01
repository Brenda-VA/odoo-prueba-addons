#addons/modulo_prueba/models/account_move.py
from odoo import fields, models, Command

''' Herencia de modelo por extensión:
       * _inherit = 'account.move' significa que NO creo un modelo nuevo (tabla en postgres), solo q modifico, añado o cambio funciones de este modelo
       * Estoy ampliando el modelo existente de Odoo account.move,en este caso, el que se usa para facturas/asientos
       * Todo lo que añada aquí, como campos o métodos, pasa a estar disponible en account.move              

    Herencia por delegación o polimorfismo:
       * _inherits = Crea un modelo nuevo (tabla en postgres) pero hereda la estructura de otro ya existente y las vincula de forma invisible con un Many2one
       * EJM:   Usuario en Odoo q tiene campos como contraseña o permisos, pero delega (_inherits) en el modelo de contactos (res.partner) 
                para tener nombre, teléfono y dirección sin tener que duplicar esos campos en la base de datos
       * Sirve si vas a crear un modelo que va a ser como un subtipo o categoría especial de otro                                                                                               '''
class AccountMove(models.Model):
    _inherit= 'account.move' #Herencia por Extensión de account, no se crea una nueva tabla, sólo se modifican y se añaden campos/funciones a la tabla facturas q ya existe

# Campo One2many añadido al modelo account.move
# Muestra todos los registros de modulo_prueba.youtube cuyo move_id apunta a esta factura
# No crea una columna nueva en account.move; usa el campo inverso move_id del modelo Youtube
    youtube_test_ids = fields.One2many(
        comodel_name='modulo_prueba.youtube', 
        inverse_name='move_id', 
        string='Youtube Test')

    ''' 
    COMANDOS ORM: 
    Cada comando es una tupla de 3 elementos donde:     * El primer elemento IDENTIFICA al comando
                                                        * El segundo es el ID de registro o un 0
                                                        * El tercer son los valores a asignar, una lista de ids o un 0   

        Numeric syntax	 |     Command syntax -> 'odoo/orm/commands.py'      -----> Ver esta forma en 'odoo/orm/commands.py' del código fuente de Odoo
      ---------------------------------------------
        (0, 0, {...})	 |  Command.create({...})
        (1, id, {...})	 |  Command.update(id, {...})
        (2, id)	         |  Command.delete(id)
        (3, id)	         |  Command.unlink(id)
        (4, id)	         |  Command.link(id)
        (5, 0, 0)	     |  Command.clear()
        (6, 0, ids)	     |  Command.set(ids)

        CREATE= 0 ->  [(0, 0, { values })]   -> Crea los valores y descripciones que indiquemos en el último elemento
        UPDATE= 1 -> [(1, {id}, { values })] -> Actualiza el id del registro {id} con el valor que le pongamos en values
        DELETE= 2 ->        [(2, {id})]      -> Elimina el registro vinculado al {id}
        UNLINK= 3 ->        [(3, {id})]      -> Corta el vínculo, osea elimina la relación entre los 2 objetos pero no elimina el objeto de destino 
        LINK= 4   ->        [(4, {id})]      -> Vincula un registro existente al campo relacional
        CLEAR= 5  ->            (5)]         -> Desvincula todos los registros relacionados del campo One2many/Many2many
        SET= 6    ->      [(6, 0, {ids})]    -> Reemplazar todas las relacionas por la lista de id's q le proporcionemos                                                            '''        

    def scm_create(self):
        #============= CREATE FORMA ANTIGUA (Sintaxis numérica) =============
        """ self.write({
                # [(0, -> El 1er 0 representa el tipo de operación, en este caso es CREATE
                # 0,   -> El 2do 0 represneta q no conocemos los ID
                # {values} -> El 3er parametro es un diccionario del cual va a obtener los valores q queremos q se creen
                'youtube_test_ids': [
                    (0, 0, {'name': 'video1', 'description':'Video1' }),
                    (0, 0, {'name': 'video2', 'description':'Video2' }),
                    (0, 0, {'name': 'video3', 'description':'Video3' })
                ]
            }) """

        #============= CREATE FORMA NUEVA (sintaxis de comandos) =============
        self.write({
                'youtube_test_ids': [
                    Command.create({'name': 'video1', 'description':'Video1' }),
                    Command.create({'name': 'video2', 'description':'Video2' }),
                    Command.create({'name': 'video3', 'description':'Video3' })
                ]
            })    

    ''' DEBUGGEAR PARA PODER SACAR LOS id's EN LA FUNCIÓN ANTES CREADA:
            1º Poner el breakpoint justo en 'self.write' de 'scm_update'
            2º Correr el debug
            3º Presionar el botón 'SMC Update' para que se ejecute la lógica de arriba
            4º Cuando se detenga en el brakpoint ir a 'Debug Console' y escribir 'self', con esto le preguntamos sobre qué registro (en este caso, Factura) se está ejecutando este método                             
            5º Si devuelve 'account.move(10,)' es como decir 'Estoy dentro de una factura/asiento de account.move cuyo ID es 10', osea self es la factura concreta desde donde pulsé el botón
            6º Al escribir 'self.youtube_test_ids', le pedimos los registros Youtube Test que tenga esta factura
            7º 'self.youtube_test_ids.ids' -> Me da sólo la lista de IDs de este registro (factura/recordset)
            8º El debugger me devuelve [3, 4, 5] (o 'modulo_prueba.youtube(3, 4, 5)' si usé 'self.youtube_test_ids')                                        '''

        #============= UPDATE FORMA ANTIGUA (Sintaxis numérica) =============
    """ def scm_update(self):
            self.write({
                # [(1, -> El 1 representa la acción UPDATE
                # x,   -> El 2do valor debe ser el id del campo que queremos actualizar
                # {values} -> El 3er parametro es un diccionario del cual va a obtener los valores q queremos q se editen y actualicen
                'youtube_test_ids': [
                    (1, 9, {'description':'Video1 Update'}),
                    (1, 10, {'name': 'video20'}),
                    (1, 11, {'name': 'video30', 'description': 'Video30'})
                ]
            })  """

    #============= UPDATE FORMA NUEVA (Sintaxis de comandos) =============
    def scm_update(self):
        self.write({
            'youtube_test_ids': [
                Command.update(15, {'description':'Video1 Update'}),
                Command.update(16, {'name': 'video20'}),
                Command.update(17, {'name': 'video30', 'description': 'Video30'})
            ]
        }) 

        #============= DELETE FORMA ANTIGUA (Sintaxis numérica) =============
    """ def scm_delete(self):
            #hay que tener cuidado con DELETE porque no solo deslinkea, si no tmb borra completamente el registro de la BBDD
            # [(2, -> El 2 representa la acción DELETE
            # x,   -> El 2do valor debe ser el id del campo que queremos BORRAR PERMANENTEMENTE de la BBDD
            self.write({ 'youtube_test_ids': [(2, 10)] }) """

 #============= DELETE FORMA NUEVA (Sintaxis de comandos) =============
    def scm_delete(self):
        self.write({ 'youtube_test_ids': [Command.delete(16)] })
        

    
    def scm_unlink(self):
        """============= UNLINK FORMA ANTIGUA (Sintaxis numérica) =============
         Igual que DELETE sólo que en lugar de borrar permanentemente el registro, sólo lo deslinkea de 'youtube_test_ids'
            [ 3(, -> El 3 representa la acción UNLINK
            x,   -> El 2do valor debe ser el id del campo que queremos DESLINKEAR 
            Al apretar el botón SCM Unlink dejamos de ver ese registro desde nuestra factura porque ya no está enlazada a ella, sin embargo si la buscamos en la bbdd vemos q existe    
            self.write({ 'youtube_test_ids': [(3, 9)] }) """
#============= UNLINK FORMA NUEVA (Sintaxis de comandos) =============
        self.write({ 'youtube_test_ids': [Command.unlink(15)] })   

        
    def scm_link(self):
        """ ============= LINK FORMA ANTIGUA (Sintaxis numérica)
            Lo contrario a Unlink. Este linkea o enlaza un registro con otro
            [( 4, -> El 4 representa la acción LINK
            x,   -> El 2do valor debe ser el id del campo que queremos LINKEAR 
            Al apretar el botón SCM Link vemos que el registro que deslinkeamos antes vuelve a nuestra factura, eso es pq no lo habíamos eliminado, y ahora podemos volver a enlazarlo
            self.write({ 'youtube_test_ids': [(4, 9)] }) """
#============= LINK FORMA NUEVA (Sintaxis de comandos) =============        
        self.write({ 'youtube_test_ids': [Command.link(15)] })

    
    def scm_clear(self):
        #============= CLEAR FORMA ANTIGUA (Sintaxis numérica) =============
        """ [(5, 0, 0)] -> El 5 representa la acción CLEAR. Sí o sí se debe de acompañar de 2 ceros
            Desvincula todos los registros relacionados del campo One2many/Many2many.
            En One2many, normalmente deja el campo inverso Many2one en NULL si el ondelete lo permite.
            self.write({ 
                    'youtube_test_ids': [(5, 0, 0)] #Como los comandos deben tener 3 elementos se rellenan con 0
                }) """

#============= CLEAR FORMA NUEVA (Sintaxis de comandos) =============   
        self.write({ 
                'youtube_test_ids': [Command.clear()]
            })    

    
    def scm_set(self):
        """ ============= SET FORMA ANTIGUA (Sintaxis numérica) =============
        Reemplaza todas las relaciones por la lista de ID's que le pongamos en el último elemento
            (6, 0, [..., ..., ...]) -> El 6 representa la acción SET
            Al apretar el botón SCM Set vemos que todos los registros de la factura vuelven a aparecer pq hemos vuelto a vincular unos registros ya existente q no estaban vinculados
            self.write({ 'youtube_test_ids': [
                    (6, 0, [9, 11])
                ] })  """       

#============= SET FORMA NUEVA (Sintaxis de comandos) =============   
        self.write({ 'youtube_test_ids': [
                Command.set([15, 17])
            ] })          

    