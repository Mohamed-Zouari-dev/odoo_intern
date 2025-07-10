{
    'name': 'ICS Interventions',
    'author': 'Mohamed Zouari',
    'category': 'Interventions',
    'summary': 'ICS Interventions',
    'description': """ """,
    'depends': [
        'sale_management',
        'account',
        'base',
        'sale',
        'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/menu.xml',
        'views/ics_interventions_view.xml',
        'views/product_views.xml',
        'views/account_move_views.xml'

    ],
    'application': True,
    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',
    'sequence': 1

}
