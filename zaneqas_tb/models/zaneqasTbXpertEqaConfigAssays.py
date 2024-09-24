# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaConfigAssays(models.Model):
    _name = "zaneqas.tb.xpert.eqa.config.assays"
    _inherit = ["mail.thread"]
    _description = "zaneqas tb xpert eqa config assays"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("supervisor", "Supervisor"),
            ("approved", "Approved"),
        ],
        default='draft',
        string="Status",
        required=True,
        tracking=True
    )

    def action_save_eqa_config_assay_as_draft(self):
        self.write({
            'state': 'draft'})

    def action_submit_eqa_config_assay_to_supervisor(self):
        self.write({'state': 'supervisor'})

    def action_supervisor_approve_eqa_config_assay(self):
        self.write({'state': 'approved'})

    def action_supervisor_send_back_eqa_config_assay(self):
        self.write({'state': 'draft'})
