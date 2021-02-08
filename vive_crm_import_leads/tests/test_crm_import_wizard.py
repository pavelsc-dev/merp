"""
    Copyright 2020 VentorTech OU
    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
"""


# Stdlib:
import binascii

# Odoo:
from odoo.addons.vive_access_rights.tests.common import SetupAccessRights
from odoo.modules.module import get_module_resource
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class ExcelWizardTestCase(SetupAccessRights):
    @classmethod
    def setUpClass(cls):
        super(ExcelWizardTestCase, cls).setUpClass()
        cls.crm_lead_model = cls.env["crm.lead"]
        cls.salesperson_id = cls.env.user
        cls.sales_team_id = cls.env["crm.team"].create({"name": "<test sale team>"})
        cls.source_id = cls.env["utm.source"].create({"name": "<test source>"})
        cls.tag_ids = cls.env["crm.lead.tag"].create({"name": "<test tag>"})
        field_model = cls.env["ir.model.fields"]
        lead_email_field = field_model.search(
            [("model", "=", "crm.lead"), ("name", "=", "email_from")]
        )
        cls.sales_manager.company_id.combined_search_aggregation_lead_field_ids = [
            4,
            lead_email_field.id,
        ]
        contact_email_field = field_model.search(
            [("model", "=", "res.partner"), ("name", "=", "email")]
        )
        cls.sales_manager.company_id.combined_search_aggregation_partner_field_ids = [
            4,
            contact_email_field.id,
        ]

    def test_final_import(self):
        lead = self.crm_lead_model.create(
            {"name": "duplicate", "email_from": "test@test.test"}
        )
        lead.active = False
        xlsx_test_file_path = get_module_resource(
            "vive_crm_import_leads", "tests", "test.xlsx"
        )
        file_content = open(xlsx_test_file_path, "rb").read()
        wizard = self.env["crm.import.wizard"].create(
            {
                "original_file": binascii.b2a_base64(file_content),
                "original_file_name": "test.xlsx",
                "salesperson_id": self.salesperson_id.id,
                "sales_team_id": self.sales_team_id.id,
                "source_id": self.source_id.id,
                "tag_ids": [(6, 0, [t.id for t in self.tag_ids])],
            }
        )
        before_count_leads = self.crm_lead_model.with_context(
            active_test=False
        ).search_count([])
        wizard.final_import()
        after_count_leads = self.crm_lead_model.with_context(
            active_test=False
        ).search_count([])
        diff_count = after_count_leads - before_count_leads
        import_history = self.env["custom.import.history"].search(
            [], order="id desc", limit=1
        )
        self.assertEquals(import_history.total_imported, 2)
        self.assertEquals(import_history.total_duplicated, 4)
        self.assertEquals(import_history.total_errors, 5)
        self.assertEquals(diff_count, 2)
        self.assertEquals(
            self.crm_lead_model.search_count([("name", "=", "correct name")]), 1
        )
        self.assertEquals(
            self.crm_lead_model.search_count(
                [("name", "=", "InStride Comprehensive Foot and Ankle Center")]
            ),
            1,
        )
