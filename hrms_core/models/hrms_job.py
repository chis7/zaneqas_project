# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields, api, _


class HRMSJob(models.Model):
    _name = "hrms.job"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Job"

    name = fields.Char(string="Job Title")
    salary_grade_id = fields.Many2one(comodel_name='hrms.salary.grade', string='Salary Grade')
    cadre_id = fields.Many2one(comodel_name='hrms.cadre', string='Cadre (Health Professionals Only)')
    who_cadre_id = fields.Many2one(comodel_name='hrms.who.cadre', string='WHO Cadre (Health Professionals Only)')
    job_classification_id = fields.Many2one(comodel_name='hrms.job.classification', string='Job Classification', required=True)
    isco_08_id = fields.Many2one(
        comodel_name='hrms.isco.08',
        string='ISCO 08 code')
    # Job Description should be implemented as SmartButton
    job_description_ids = fields.One2many(
        comodel_name='hrms.job.description',
        inverse_name='hrms_job_id',
        string='Job Description')
    has_job_description = fields.Boolean(string='Has Job Description', compute='_compute_has_job_description')
    job_position_ids = fields.One2many(
        comodel_name='hr.job',
        inverse_name='hrms_job_id',
        string='Job Positions'
    )


    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Job title should be unique!')]

    @api.depends('job_description_ids')
    def _compute_has_job_description(self):
        for record in self:
            record.has_job_description = bool(record.job_description_ids)

    def action_view_hrms_job_description(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Job Description'),
            'res_model': 'hrms.job.description',
            'view_mode': 'form',
            'res_id': self.job_description_ids.id,
            'target': 'current',
        }



