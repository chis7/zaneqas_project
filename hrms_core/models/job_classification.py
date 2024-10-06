# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class JobClassification(models.Model):
    _name = "hrms.job.classification"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Job Classification"

    name = fields.Char('Name')
    description = fields.Text('Description')
    code = fields.Char('Code')
    hrms_job_ids = fields.One2many(
        comodel_name='hrms.job',
        inverse_name='job_classification_id',
        string='Jobs'
    )

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]