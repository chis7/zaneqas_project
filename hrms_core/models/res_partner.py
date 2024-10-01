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

    company_type = fields.Selection(
        string='Company Type',
        selection_add=[
            ('mpsa', 'MPSA'),
            ('training_institution', 'Training Institution'),
        ],
        compute='_compute_company_type',
        inverse='_write_company_type')
    # is_mpsa = fields.Boolean(
    #     string='Contact is an MPSA',
    #     default=False,
    #     help="Check if the contact is a MPSA")
    # is_training_institution = fields.Boolean(
    #     string='Contact is a Training Institution',
    #     default=False,
    #     help="Check if the contact is a Training Institution")


    # @api.depends('is_company', 'is_mpsa', 'is_training_institution')
    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            if partner.is_company:
                partner.company_type = 'company'
            # if partner.is_company:
            #     partner.company_type = 'mpsa'
            # elif partner.is_training_institution:
            #     partner.company_type = 'training_institution'
            else:
                partner.company_type = 'person'

    def _write_company_type(self):
        for partner in self:
            partner.is_company = (partner.company_type == 'company')
            # partner.is_company = (partner.company_type == 'mpsa')
            # partner.is_training_institution = (partner.company_type == 'training_institution')

    @api.onchange('company_type')
    def onchange_company_type(self):
        if self.company_type == 'company':
            self.is_company = True
            # self.is_mpsa = False
            # self.is_training_institution = False
        # elif self.company_type == 'mpsa':
        #     self.is_mpsa = True
        #     self.is_company = False
        #     self.is_training_institution = False
        # elif self.company_type == 'training_institution':
        #     self.is_training_institution = True
        #     self.is_company = False
        #     self.is_mpsa = False
        # else:
        #     self.is_company = False
        #     self.is_mpsa = False
        #     self.is_training_institution = False
