# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class WHOCadreCategory(models.Model):
    _name = "hrms.who.cadre.category"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = 'WHO Cadre Category'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    who_cadre_ids = fields.Many2many(comodel_name='hrms.who.cadre', string='Who Cadres')

class WHOCadre(models.Model):
    _name = 'hrms.who.cadre'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = 'Classifying health workers: Mapping occupations to the international standard classification'
    _rec_name = 'occupation_group'

    isco_08_id = fields.Many2one(comodel_name='hrms.isco.08', string='ISCO 08 Code')
    who_cadre_category_id = fields.Many2one(comodel_name='hrms.who.cadre.category', string='Who Cadre Category', required=True)
    occupation_group = fields.Char(string='Occupation Group', required=True)
    definition = fields.Text(string='Definition', required=True)
    examples = fields.Text('Examples')
    notes = fields.Text('Notes')
    hrms_job_ids = fields.One2many(
        comodel_name='hrms.job',
        inverse_name='who_cadre_id',
        string='Jobs'
    )

