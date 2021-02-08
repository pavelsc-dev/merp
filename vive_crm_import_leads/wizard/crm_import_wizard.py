"""
    Copyright 2020 VentorTech OU
    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
"""

# Stdlib:
import logging
from collections import defaultdict
from enum import IntEnum

# Odoo:
from odoo import _, fields, models
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


HEADERS = [
    "Company Name",
    "Website",
    "Phone Number",
    "Street",
    "Street 2",
    "Zip",
    "City",
    "State",
    "Email",
    "Doctor Name",
    "Notes",
    "Validation Status",
    "error",
]

LEAD_FIELDS = [
    "name",
    "website",
    "phone",
    "street",
    "street2",
    "zip",
    "city",
    "state_id/.id",
    "email_from",
    "contact_name",
    "description",
]


# sorted as LeadIndex class
class LeadIndex(IntEnum):
    """ Index number in the list """

    COMPANY_NAME = 0
    WEBSITE = 1
    PHONE_NUMBER = 2
    STREET = 3
    STREET_2 = 4
    ZIP = 5
    CITY = 6
    STATE = 7
    EMAIL = 8
    DOCTOR_NAME = 9
    NOTES = 10


DB_DUBL_FIELDS_MAP = {
    "email": LeadIndex.EMAIL,
    "email_from": LeadIndex.EMAIL,
    "phone_normalized": LeadIndex.PHONE_NUMBER,
    "mobile_normalized": LeadIndex.PHONE_NUMBER,
}


class ExcelWizard(models.TransientModel):
    """ Allows you to import leads without duplicates and errors """

    _inherit = "custom.import.wizard"
    _name = "crm.import.wizard"
    _description = "Wizard for import leads in CRM"

    salesperson_id = fields.Many2one("res.users")
    sales_team_id = fields.Many2one(
        "crm.team",
        domain=[("use_leads", "=", True)],
        string="Customer Industry",
    )
    source_id = fields.Many2one("utm.source")
    tag_ids = fields.Many2many(
        "crm.tag",
        string="Tags",
        help="Classify and analyze your lead/opportunity categories like: Training, Service",
    )

    # pylint: disable=no-self-use
    def _get_model_name(self):
        return "crm.lead"

    def _get_extra_info(self):
        salesperson_id = self.salesperson_id.name_get()
        sales_team_id = self.sales_team_id.name_get()
        source_id = self.source_id.name_get()
        tag_ids = self.tag_ids.name_get()
        extra_info = _(
            "salesperson_id: {}\n"
            "sales_team_id: {}\n"
            "source_id: {}\n"
            "tag_ids: {}\n"
        ).format(salesperson_id, sales_team_id, source_id, tag_ids)
        return extra_info

    def _check_required_fields(self):
        self.ensure_one()
        if not all(
            [
                self.original_file,
                self.salesperson_id,
                self.sales_team_id,
                self.source_id,
            ]
        ):
            raise ValidationError(_("Please fill in first four fields"))

    # pylint: disable=no-self-use
    def _get_sample_file_path(self):
        xlsx_file_path = get_module_resource(
            "vive_crm_import_leads", "static", "sample_import_file.xlsx"
        )
        return xlsx_file_path

    def read_original_line(self, row):
        """ This method is for formatting raw data from a cell """

        line = {"values": [], "errors": [], "status": "success"}
        for cell in row:
            if isinstance(cell.value, float):
                line["values"].append(str(int(cell.value)))
            else:
                line["values"].append(str(cell.value))
        return line

    def normalize_fields(self, leads):
        """
            Replace all phones by pattern

            Args:
                leads (dict): leads that will be checked

            Returns:
                dict: formatted leads
        """

        for lead in leads:
            phone = lead["values"][LeadIndex.PHONE_NUMBER]
            if phone and not phone.startswith("+1"):
                phone = "+1{}".format(phone)
            lead["values"][LeadIndex.PHONE_NUMBER] = phone
        return leads

    def find_duplicates_in_file(self, leads):
        """
            Look for duplicates for leads from file in file

            Args:
                leads (dict): leads that will be checked

            Returns:
                dict: formatted leads
        """

        search_fields = []

        # Gather indexes of fields which are used to find duplicates
        findexes = []
        if "phone_normalized" in search_fields or "mobile_normalized" in search_fields:
            findexes.append(LeadIndex.PHONE_NUMBER)
        if "email_from" in search_fields:
            findexes.append(LeadIndex.EMAIL)

        duplicates = defaultdict(lambda: defaultdict(int))

        # Calculate Duplicates
        for lead in leads:
            for index in findexes:
                value = str(lead["values"][index])
                if value.strip():
                    duplicates[index][value] += 1

        # Write duplicate info to the Lead
        for lead in leads:
            for index in findexes:
                if duplicates[index][lead["values"][index]] > 1:
                    lead["errors"].append(
                        _("Duplicated in file by {fname}").format(fname=HEADERS[index])
                    )
                    lead["status"] = "duplicate"
        return leads

    def find_duplicates_in_model(self, leads, model, setting):
        """
            Look for duplicates for leads from file in db from specify model

            Args:
                leads (dict): leads that will be checked

            Returns:
                dict: formatted leads
        """

        search_fields = getattr(self.env.user.company_id, setting).mapped("name")
        for lead in leads:
            cond = []
            for fname, index in DB_DUBL_FIELDS_MAP.items():
                if fname in search_fields:
                    cond.append((fname, "=", lead["values"][index]))
            if cond:
                cond = ["|"] * (len(cond) - 1) + cond
                res = self.env[model].with_context(active_test=False).search_count(cond)
                if res > 0:
                    lead["errors"].append(
                        _("Found {num} duplicates in {model}").format(
                            num=res, model=model
                        )
                    )
                    lead["status"] = "duplicate"
        return leads

    def find_duplicates_in_db(self, leads):
        """
            Look for duplicates for leads from file in db

            Args:
                leads (dict): leads that will be checked

            Returns:
                dict: formatted leads
        """
        return leads

    def validate_line_state(self, line):
        """
            Validating state, if incorrect then writing error message

            Args:
                line (dict): lead that will be checked

            Returns:
                dict: formatted lead
        """

        state_model = self.env["res.country.state"]
        usa_country_id = self.env.ref("base.us").id
        state_code = line["values"][LeadIndex.STATE].upper()
        if state_code:
            state = state_model.search(
                [("code", "=", state_code), ("country_id", "=", usa_country_id)]
            )
            if len(state) == 1:
                line["to_write"][LeadIndex.STATE] = state.id
            else:
                line["errors"].append(_("Incorrect State code"))
                line["status"] = "error"
        else:
            line["errors"].append(_("Empty State code"))
            line["status"] = "error"
        return line

    def validate_line_company_name(self, line):
        """
            Validating company name, if incorrect then writing error message

            Args:
                line (dict): lead that will be checked

            Returns:
                dict: formatted lead
        """

        company_name = line["values"][LeadIndex.COMPANY_NAME]
        if not company_name:
            line["errors"].append(_("Empty Company Name"))
            line["status"] = "error"
        return line

    def validate_line_phone(self, line):
        """
            Validating phone, if incorrect then writing error message

            Args:
                line (dict): lead that will be checked

            Returns:
                dict: formatted lead
        """

        phone = line["values"][LeadIndex.PHONE_NUMBER]
        if not phone:
            line["errors"].append(_("Empty Phone"))
            line["status"] = "error"
        return line

    def validate_lines(self, leads):
        """
            Validating lines, if incorrect then writing error message

            Args:
                leads (dict): leads that will be checked

            Returns:
                dict: formatted leads
        """
        for lead in leads:
            lead["to_write"] = lead["values"].copy()
            lead = self.validate_line_state(lead)
            lead = self.validate_line_company_name(lead)
            lead = self.validate_line_phone(lead)
        return leads

    def load(self, leads):
        """ Importing correct leads """

        correct_leads = filter(lambda l: l["status"] == "success", leads)
        import_result = self.env["crm.lead"].load(
            LEAD_FIELDS, [lead["to_write"] for lead in correct_leads]
        )
        lead_ids = self.env["crm.lead"].browse(import_result["ids"])
        lead_ids.write(
            {
                "user_id": self.salesperson_id.id,
                "source_id": self.source_id.id,
                "tag_ids": [(6, 0, [t.id for t in self.tag_ids])],
            }
        )
        lead_ids.write({"team_id": self.sales_team_id.id})
        return import_result

    def handle_import(self, test=True):
        """
            Do some checks for leads

            Args:
                test (bool, optional): If False then write leads to db. Defaults to True.
        """

        leads = self.read_original_file()
        leads = self.normalize_fields(leads)
        leads = self.find_duplicates_in_file(leads)
        leads = self.find_duplicates_in_db(leads)
        leads = self.validate_lines(leads)
        if not test:
            self.load(leads)

        self.write_result_file(HEADERS, leads)

        return leads

    def final_import(self):
        """ Importing correct leads """

        self._check_required_fields()
        return super(ExcelWizard, self).final_import()
