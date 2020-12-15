# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Ventor Default Locations',
    "version": "13.0.1.0.0",
    'author': 'VentorTech',
    'website': 'https://ventor.tech/',
    'license': 'LGPL-3',
    'installable': True,
    'images': ['static/description/main_banner.png'],
    'summary': 'Adding small improvements to Locations',
    'depends': [
        'merp_base',
        'merp_custom_access_rights'
    ],
    'data': [
        'views/res_config.xml',
        'views/res_users.xml',
        'views/stock_inventory.xml',
        'views/stock_warehouse.xml',
    ],
}
