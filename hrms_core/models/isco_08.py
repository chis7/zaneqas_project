# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class ISCO08(models.Model):
    _name = "hrms.isco.08"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "International Standard Classification of Occupations (ISCO) 08 Code"
    _rec_name = 'unit'

    ISCO_version = fields.Char(string='ISCO Version')
    major = fields.Char(string='Major', required=True)
    major_label = fields.Char(string='Major Label', required=True)
    sub_major = fields.Char(string='Sub Major', required=True)
    sub_major_label = fields.Char(string='Sub Major Label', required=True)
    minor = fields.Char(string='Minor', required=True)
    minor_label = fields.Char(string='Minor Label', required=True)
    unit = fields.Char(string='Unit', required=True)
    description = fields.Text(string='Description', required=True)
    hrms_job_ids = fields.One2many(
        comodel_name='hrms.job',
        inverse_name='isco_08_id',
        string='Jobs'
    )
