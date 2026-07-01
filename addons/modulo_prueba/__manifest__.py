# addons/modulo_prueba/__manifest__.py
# el único campo obligatorio de este archivo es el name
#sirve para declarar este módilo y especificar sus metadatos, por ejm:
#        - nombre (línea 9)
#        - descripcion (línea 13)
#        - versión de la app/módulo (línea 24)
#        - dependencias de otros módulos (línea 27)

{
    'name': "modulo_prueba",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account' 
    ],
    # ejemplo de añadir dependencias a otros módulos
    # 'depends': [
    #       'base',
    #       'purchase',
    # ],

    # always loaded
    #indica dónde se encuentran los archivos .xml, .csv, etc
    'data': [
        'security/ir.model.access.csv',
        'security/task_security.xml', #añadimos las teglas tmb al manifest
        'views/student_views.xml',
        'views/task_views.xml',
        'views/menus.xml',
        'views/account_move_views.xml',
        #'views/views.xml',
        #'views/templates.xml',
        #falta añadir el csv actualizado
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
#si agregamos una hoja de estilos se debe de meter en 'assets'
    'assets':{ 
        'web.assets_backend': [
            'modulo_prueba/static/src/css/task_kanban.css',
        ],
    }
}

