# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health GRZ
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    uid = fields.Char(string='UID')
    code = fields.Char(string='Code')
    short_name = fields.Char(string='Short Name')
    opening_date = fields.Date(string='Opening Date', default=fields.Date.today())
    closing_date = fields.Date(string='Closing Date')
    child_ids = fields.One2many('res.company', 'parent_id', string='Organisation Units')
    organisation_unit_level_id = fields.Many2one(comodel_name='hrms.organisation.unit.level', string='Organisation Unit Level')
    strategic_plan_ids = fields.One2many('hrms.strategic.plan', 'company_id', string='Strategic Plans')

