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

from odoo import models, fields, api


class CompetencyType(models.Model):
    _name = "hrms.competency.type"
    _description = "Competency Type"

    name = fields.Char(string="Name")
    competency_ids = fields.One2many(comodel_name='hrms.competency', string="Competency")

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]


class Competency(models.Model):
    _name = "hrms.competency"
    _description = "Competency"

    sequence = fields.Char(
        string='Reference',
        required=True, copy=False, readonly=True, index=True,
        default=lambda self: 'New')
    name = fields.Char(string='Name')
    competency_type_id = fields.Many2one(comodel_name='hrms.competency.type', string='Competency Type')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active')

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hrms.competency.seq') or 'New'
            result = super(Competency, self).create(vals_list)
            return result