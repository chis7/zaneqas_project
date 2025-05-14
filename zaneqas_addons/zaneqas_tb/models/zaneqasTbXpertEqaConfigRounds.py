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
    supervisor_id = fields.Many2one('res.users', string="Assigned Supervisor")
    zaneqas_tb_xpert_eqa_sample_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.rounds.sample.lines', 'config_round_id', string="Expected Results"
    )
    sample_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.rounds.sample.lines', 'config_round_id', string="Sample IDs"
    )

    def generate_sample_ids(self):
        if self.name:
            year = datetime.now().year
            round_1 = self.env['zaneqas.tb.xpert.eqa.config.rounds'].search([('name', '=', f'{year} Round 1')], limit=1)
            round_2 = self.env['zaneqas.tb.xpert.eqa.config.rounds'].search([('name', '=', f'{year} Round 2')], limit=1)
            if self.name == round_1.name:
                self.zaneqas_tb_xpert_eqa_sample_ids = [
                    (0, 0, {'sample_id': f'CDL PT ROUND 1 {year} A-{i}'}) for i in range(1, 6)
                ]

            elif self.name == round_2.name:
                self.zaneqas_tb_xpert_eqa_sample_ids = [
                    (0, 0, {'sample_id': f'CDL PT ROUND 2 {year} B-{i}'}) for i in range(1, 6)
                ]
            self.write({'sample_ids': self.zaneqas_tb_xpert_eqa_sample_ids})

    def action_save_eqa_config_round_as_draft(self):
        current_year = datetime.now().year
        # record = super(ZaneqasTbXpertEqaConfigRounds, self).create(vals)

        self.write({
            'state': 'draft',
            'name': f"{current_year} {self.name}"
        })
        self.generate_sample_ids()
        # return record

    def action_submit_eqa_config_round_to_supervisor(self):
        self.write({'state': 'supervisor'})
        group = self.env.ref("zaneqas_tb.group_cdl_supervisor_approve_site_eqa_expected_results")
        users = group.users

        if users:
            selected_user = random.choice(users)
            self.supervisor_id = selected_user.id
            if selected_user.email:
                mail_values = {
                    'subject': 'Request for Approval',
                    'body_html': """<p>You have received a request for approval of an EQA configuration. Click <a href='http://localhost:8069'>here</a> to log in and access the request.</p>""",
                    'email_to': selected_user.email,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()

    def action_supervisor_approve_eqa_config_round(self):
        if self.env.user != self.supervisor_id:
            raise models.ValidationError("You are not authorized to approve this EQA configuration round.")
        current_year = datetime.now().year
        self.write({'state': 'approved', 'name': f"{current_year} {self.name}"})
        user = self.create_uid.email
        if user:
            mail_values = {
                'subject': 'Your Request for Approval',
                'body_html': """<p>Your EQA configuration has been approved. Click <a href='http://localhost:8069'>here</a> to log in and check the status.</p>""",
                'email_to': user,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

    def action_supervisor_send_back_eqa_config_round(self):
        self.write({'state': 'draft'})
        user = self.create_uid.email
        if user:
            mail_values = {
                'subject': 'Your Request for Approval',
                'body_html': """<p>Your EQA configuration has been sent back for your review. Click <a href='http://localhost:8069'>here</a> to log in and check the status.</p>""",
                'email_to': user,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()
