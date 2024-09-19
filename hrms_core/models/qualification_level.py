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


class QualificationLevel(models.Model):
    _name = "hrms.qualification.level"
    _description = "Qualification Levels and the Sub-frameworks of the Zambia Qualification Framework"

    name = fields.Char(string="Name")
    typical_qualification_type = fields.Char(string="Typical Qualification Type")
    zqf_sub_framework = fields.Selection(
        selection=[
            ('general_education', 'General Education'),
            ('tevet', 'TEVET'),
            ('higher_education', 'Higher Education'),
        ],
        string="ZQF Sub-framework")
    standard_duration = fields.Char(string="Standard Duration")
    qualification_ids = fields.One2many(
        comodel_name='hrms.qualification',
        inverse_name='qualification_level_id',
        string="Qualifications")
    competence_ids = fields.One2many(
        comodel_name='hrms.competence',
        inverse_name='qualification_level_id',
        string='Competences')

