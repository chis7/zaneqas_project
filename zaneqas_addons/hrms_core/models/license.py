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


class License(models.Model):
    _name = "hrms.license"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "License"

    name = fields.Char(string="Name")
    registration_authority = fields.Many2one(
        comodel_name="res.partner",
        string="Registration Authority"
    )


    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]



