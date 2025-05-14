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
        group = self.env.ref("zaneqas_tb.group_cdl_supervisor_approve_site_eqa_expected_results")

        users = group.users

        if users:
            selected_user = random.choice(users)
            if selected_user.email:

                mail_values = {
                    'subject': 'Request for Approval',
                    'body_html': """<p>You have received a request for approval of an EQA configuration. Click <a href='http://localhost:8069'>here</a> to log in and access the request.</p>""",
                    'email_to': selected_user.email,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()

            else:
                pass
        else:
            pass

    def action_supervisor_approve_eqa_config_assay(self):
        self.write({'state': 'approved'})
        user = self.create_uid.email
        if user:
            mail_values = {
                'subject': 'Your Request for Approval',
                'body_html': """<p>Your EQA configuration has been approved. Click <a href='http://localhost:8069'>here</a> to log in and check the status.</p>""",
                'email_to': user,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

    def action_supervisor_send_back_eqa_config_assay(self):
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
