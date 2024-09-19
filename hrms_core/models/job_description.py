# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class KeyResultArea(models.Model):
    _name = 'hrms.key.result.area'
    _description = 'Job Description'

    name = fields.Char(string='Name')
    principal_accountability_ids = fields.One2many(
        comodel_name='hrms.principal.accountability',
        inverse_name='key_result_area_id',
        string='Principal Accountabilities'
    )

class PrincipalAccountability(models.Model):
    _name = 'hrms.principal.accountability'
    _description = 'Principal Accountability'

    name = fields.Char(string='Name')
    key_result_area_id = fields.Many2one(comodel_name='hrms.key.result.area', string='Key Result Area')

class Responsibility(models.Model):
    _name = 'hrms.responsibility'
    _description = 'Responsibility'

    name = fields.Char(string='Name')


class JobDescription(models.Model):
    _name = 'hrms.job.description'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = 'Job Description'

    name = fields.Char(related='hrms_job_id.name', string='Job Position', required=True, store=True)
    hrms_job_id = fields.Many2one(comodel_name='hrms.job', string='Job', required=True)
    department_id = fields.Many2one(comodel_name='hr.department', string='Department', required=True)
    job_purpose = fields.Html(string='Job Purpose')
    principal_accountability_ids = fields.Many2many(comodel_name='hrms.principal.accountability', string='Principal Accountabilities')
    responsibility_ids = fields.Many2many(comodel_name='hrms.responsibility', string='Responsibilities')
    qualification_ids = fields.Many2many(comodel_name='hrms.qualification', string='Qualifications')
    skill_ids = fields.Many2many(comodel_name='hr.skill', string='Required Skills')
    experience = fields.Html(string='Experience')
    reports_to = fields.Many2one(comodel_name='hr.employee', string='Reports To')
    job_level = fields.Selection(
        selection=[
            ('entry', 'Entry Level'),
            ('mid', 'Mid Level'),
            ('senior', 'Senior Level'),
            ('executive', 'Executive Level')
        ],
        string='Job Level',
        required=True,
        default='entry'
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
        ],
        string='State',
    )

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]


