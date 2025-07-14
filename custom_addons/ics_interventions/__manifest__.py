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
        'product']
    ,
    'data': [
        'data/intervention_data.xml',
        'security/ir.model.access.csv',
        'report/report_intervention.xml',
        'views/product_views.xml',
        # 'views/account_move_views.xml',
        'views/ics_interventions_view.xml',
        'views/actions.xml',
        'views/menus.xml',

    ],
    'application': True,
    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',
    'sequence': 1

}
