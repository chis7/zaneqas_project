# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class Cadre(models.Model):
    _name = "hrms.cadre"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Cadre"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    hrms_job_ids = fields.One2many(
        comodel_name='hrms.job',
        inverse_name='cadre_id',
        string='Jobs'
    )
    user_id = fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.user)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]
