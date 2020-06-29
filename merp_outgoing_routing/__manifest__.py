# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

{
    'name': 'Picking and Reservation Strategy',
    "version": "11.0.1.0.0",
    'author': 'VentorTech',
    'website': 'https://ventor.tech/',
    'license': 'LGPL-3',
    'installable': True,
    'images': ['static/description/images/image1.JPG'],
    'summary': 'Allows to automatically build optimal picking routes and apply custom reservation options',
    'depends': [
        'merp_base',
    ],
    'data': [
        'views/res_config.xml',
        'views/stock.xml',
        'views/picking.xml'
    ],
}
