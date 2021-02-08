# pylint: disable=missing-docstring
# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Vive Health Import Leads",
    "category": "Accounting",
    "version": "12.0.1.0.0",
    "website": "https://ventor.tech",
    "author": "VentorTech OU",
    "license": "LGPL-3",
    "depends": [
        # =========================
        # odoo modules:
        # =========================
        'crm',
        # =========================
        # external modules:
        # =========================
        # =========================
        # ventor.tech modules:
        # =========================
        'custom_import_wizard',
        # =========================
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/custom_import_history.xml",
        "wizard/crm_import_wizard.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
