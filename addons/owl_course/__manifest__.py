{
    'name': "owl_course",

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

    # Los componentes de odoo siempre dependen de base y web
    'depends': ['base', 'web'],

    # AQUÍ DEBEMOS DECLARAR TODOS LOS ARCHIVOS QUE VAMOS A UTILIZAR EN EL MÓDULO, YA SEA XML, JS, CSS, ETC...
    'data': [
        # 'security/ir.model.access.csv',
        'views/menus.xml',
        'views/user_actions.xml',
        'views/hello_world_actions.xml'
    ],
    'assets':{ 
        'web.assets_backend': [
            'owl_course/static/src/**/*',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}