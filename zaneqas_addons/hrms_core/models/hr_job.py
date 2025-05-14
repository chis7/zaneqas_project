# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields, api


class Job(models.Model):
    _inherit = 'hr.job'
    _description = "Position"

    name = fields.Char(related='hrms_job_id.name', string='Title', store=True, readonly=True)
    hrms_job_id = fields.Many2one(
        comodel_name='hrms.job',
        string='Job'
    )
    post_id = fields.Char(string='Position ID', help='PEMIC Position ID')
    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency', compute='_compute_currency_id')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', index=True)
    salary_source_id = fields.Many2one(comodel_name='hrms.funder', string='Salary Source')
    proposed_salary = fields.Monetary(string='Proposed Salary', currency_field='currency_id')
    supervisor_id = fields.Many2one(comodel_name='hr.employee', string='Supervisor')
    department_id = fields.Many2one(comodel_name='hr.department', string='Department')
    proposed_hiring_date = fields.Date(string='Proposed Hiring Date')
    proposed_end_date = fields.Date(string='Proposed End Date')
    state = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('closed', 'Closed'),
            ('discontinued', 'Discontinued'),
        ],
        string='State',
        default='open',
    )

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for job_position in self:
            job_position.currency_id = job_position.company_id.sudo().currency_id.id or main_company.currency_id.id
