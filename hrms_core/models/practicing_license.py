# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class ProfessionBody(models.Model):
    _name = "hrms.profession.body"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Profession Body"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    user_id = fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.user)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]


class PracticingLicense(models.Model):
    _name = "hrms.practicing.license"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Practicing License"
    _rec_name = 'license_number'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    license_number = fields.Char(string='Licence Number')
    issue_date = fields.Date(string='Issue Date')
    expiry_date = fields.Date(string='Expiry Date')
    profession_body_id = fields.Many2one(comodel_name='hrms.profession.body', string='Profession Body')

    _sql_constraints = [
        ('unique_license_number',
         'unique(license_number)', 'License number should be unique!')]


