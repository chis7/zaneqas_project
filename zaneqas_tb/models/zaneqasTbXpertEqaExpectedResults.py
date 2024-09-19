# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaExpectedResults(models.Model):
    _name = "zaneqas.tb.xpert.eqa.expected.result"
    _inherit = ["mail.thread"]
    _description = "zaneqas tb xpert eqa expected results"
    name = fields.Many2one("zaneqas.tb.xpert.eqa.config.rounds", required=True)
    due_date = fields.Date(string="Due Date", required=True)
    zaneqas_tb_xpert_eqa_expected_result_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.expected.result.lines',
        'zaneqas_tb_xpert_eqa_expected_result_id',
        string="ZANEQAS TB Xpert EQA Results Lines"
    )
    expected_result_lines_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.expected.result.lines',
        'zaneqas_tb_xpert_eqa_expected_result_id',
        string="Expected Result Lines"
    )

    @api.onchange('name')
    def _onchange_name(self):
        self.zaneqas_tb_xpert_eqa_expected_result_ids = [(5, 0, 0)]  # Clear existing values
        if self.name:
            year = datetime.now().year
            round_1 = self.env['zaneqas.tb.xpert.eqa.config.rounds'].search([('name', '=', f'{year} Round 1')], limit=1)
            round_2 = self.env['zaneqas.tb.xpert.eqa.config.rounds'].search([('name', '=', f'{year} Round 2')], limit=1)
            if self.name == round_1:
                self.zaneqas_tb_xpert_eqa_expected_result_ids = [
                    (0, 0, {'sample_id': 'A1'}),
                    (0, 0, {'sample_id': 'A2'}),
                    (0, 0, {'sample_id': 'A3'}),
                    (0, 0, {'sample_id': 'A4'}),
                    (0, 0, {'sample_id': 'A5'}),
                ]
            elif self.name == round_2:
                self.zaneqas_tb_xpert_eqa_expected_result_ids = [
                    (0, 0, {'sample_id': 'B1'}),
                    (0, 0, {'sample_id': 'B2'}),
                    (0, 0, {'sample_id': 'B3'}),
                    (0, 0, {'sample_id': 'B4'}),
                    (0, 0, {'sample_id': 'B5'}),
                ]

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("supervisor", "Supervisor"),
            ("lab_incharge", "Lab Incharge"),
            ("approved", "Approved"),
            ("published", "Published"),
        ],
        default='draft',
        string="Status",
        required=True,
        tracking=True

    )
    supervisor_comment = fields.Char(string="Supervisor Comment", tracking=True)
    lab_incharge_comment = fields.Char(string="Lab Incharge Comment", tracking=True)


    def action_save_eqa_result_as_draft(self):
        self.write({'state': 'draft'})

    def action_submit_eqa_result_to_supervisor(self):
        self.write({'state': 'supervisor'})

    def action_supervisor_approve_eqa_result(self):
        self.write({'state': 'lab_incharge'})

    def action_supervisor_send_back_eqa_result(self):
        self.write({'state': 'draft'})

    def action_LabIncharge_send_back_eqa_result(self):
        self.write({'state': 'lab_incharge'})

    def action_LabIncharge_approve_eqa_result(self):
        self.write({'state': 'approved'})
