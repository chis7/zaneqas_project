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

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class EmployeeLicense(models.Model):
    _name = "hrms.employee.license"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = "Employee License"

    name = fields.Char(string="Employee Name", related='employee_id.name')
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Employee",
        required=True, ondelete='cascade', index=True, copy=False,
        default=lambda self: self.env.context.get('employee_id.id', None)
    )
    license_id = fields.Many2one(
        comodel_name='hrms.license',
        string="License"
    )
    license_number = fields.Char(string="License Number", required=True, tracking=True)
    license_name = fields.Char(string='License Name', compute='_compute_license_name')
    issue_date = fields.Date(string="Issue Date", required=True, tracking=True)
    expiry_date = fields.Date(string="Expiry Date", required=True, tracking=True)
    certificate = fields.Binary(string="Certificate", tracking=True)
    state = fields.Selection(
        selection=[
            ('expired', 'Expired'),
            ('expiring', 'Expiring'),
            ('valid', 'Valid')],
        compute='_compute_state', store=True
    )
    license_scheduled_activity = fields.Boolean(default=False)

    @api.depends('expiry_date')
    def _compute_state(self):
        self.state = 'valid'
        for line in self:
            if line.expiry_date:
                if line.expiry_date <= fields.Date.today():
                    line.state = 'expired'
                elif line.expiry_date + relativedelta(months=-3) <= fields.Date.today():
                    line.state = 'expiring'

    @api.depends('name', 'license_number')
    def _compute_license_name(self):
        for employee in self:
            name = employee.name.replace(' ', '_') + '_' if employee.name else ''
            license_number = '_' + employee.license_number if employee.license_number else ''
            employee.license_name = "%slicense%s" % (name, license_number)



