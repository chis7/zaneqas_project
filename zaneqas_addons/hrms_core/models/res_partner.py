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


class Partner(models.Model):
    _inherit = "res.partner"

    is_mpsa = fields.Boolean(
        string='Contact is an MPSA',
        default=False,
        help="Check if the contact is a MPSA")
    is_training_institution = fields.Boolean(
        string='Contact is a Training Institution',
        default=False,
        help="Check if the contact is a Training Institution")

