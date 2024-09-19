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


class QualificationLine(models.Model):
    _name = "hrms.qualification.line"
    _description = "Qualification Line"

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Employee",
        required=True, ondelete='cascade', index=True, copy=False)
    qualification_id = fields.Many2one(
        comodel_name='hrms.qualification',
        string="Qualification")
    training_institution_id = fields.Many2one(
        comodel_name='res.partner',
        string="Training Institution")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")



