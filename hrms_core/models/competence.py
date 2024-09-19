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


class Competence(models.Model):
    _name = "hrms.competence"
    _description = "Competence"
    _rec_name = 'sequence'

    sequence = fields.Char(
        string='Reference',
        required=True, copy=False, readonly=True, index=True,
        default=lambda self: 'New')
    competence_type = fields.Selection(
        selection=[
            ('foundational_competence', 'Foundational Competence'),
            ('practical_competence', 'Practical Competence'),
            ('reflexive_competence', 'Reflexive Competence'),
        ],
        string="Competence Type")
    description = fields.Text('Description')
    qualification_level_id = fields.Many2one(comodel_name='hrms.qualification.level', string="Qualification Level")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hrms.competence.seq') or 'New'
            result = super(Competence, self).create(vals_list)
            return result