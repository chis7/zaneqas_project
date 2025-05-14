# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields


class SalarySource(models.Model):
    _name = "hrms.funder"
    _description = "Funder"

    name = fields.Char(string='Name', required=True)
    short_name = fields.Char('Short Name')

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]
