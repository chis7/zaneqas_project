# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class KeyResultArea(models.Model):
    _name = "hrms.job.key.result.area"
    _description = "Key Result Area"

    name = fields.Char('Name', size=256, required=True)
    district_ids = fields.Many2many(
        comodel_name='hrms.district',
        relation='province_district_relation',
        column1='province_id',
        column2='district_id',
        string='Districts'
    )
    user_id = fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.user)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]
