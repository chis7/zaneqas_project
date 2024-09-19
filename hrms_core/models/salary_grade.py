# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields, api


class SalaryGrade(models.Model):
    _name = "hrms.salary.grade"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Salary Grade"

    name = fields.Char('Name')
    currency_id = fields.Many2one(
        'res.currency', 'Currency', compute='_compute_currency_id')
    company_id = fields.Many2one(
        'res.company', 'Company', index=True)
    start = fields.Monetary('Start', currency_field="currency_id")
    mid_point = fields.Monetary('Mid Point', currency_field="currency_id")
    end = fields.Monetary('End', currency_field="currency_id")
    notes = fields.Text('Notes')
    hrms_job_ids = fields.One2many(
        comodel_name='hrms.job',
        inverse_name='salary_grade_id',
        string='Jobs'
    )

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for salary_grade in self:
            salary_grade.currency_id = salary_grade.company_id.sudo().currency_id.id or main_company.currency_id.id
