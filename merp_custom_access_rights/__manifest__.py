# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Ventor Custom Access Rights',
    "version": "14.0.1.0.0",
    'author': 'VentorTech',
    'website': 'https://ventor.tech/',
    'license': 'LGPL-3',
    'installable': True,
    'images': ['static/description/main_banner.png'],
    'summary': 'Ventor Custom Access Rights',
    'depends': [
        'merp_base',
    ],
    'data': [
        'security/groups.xml',
        'views/res_users.xml',
    ],
}
