# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaConfigRounds(models.Model):
    _name = "zaneqas.tb.xpert.eqa.config.rounds"
    _inherit = ["mail.thread"]
    _description = "zaneqas tb xpert eqa config rounds"

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

    def action_save_eqa_config_round_as_draft(self):
        current_year = datetime.now().year
        self.write({
            'state': 'draft',
            'name': f"{current_year} {self.name}"
        })

    def action_submit_eqa_config_round_to_supervisor(self):
        self.write({'state': 'supervisor'})

    def action_supervisor_approve_eqa_config_round(self):
        self.write({'state': 'Approved'})

    def action_supervisor_send_back_eqa_config_round(self):
        self.write({'state': 'draft'})
