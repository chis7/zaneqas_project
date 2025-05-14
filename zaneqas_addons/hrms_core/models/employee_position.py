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
from email.policy import default

from odoo import models, fields, api


class EmployeePosition(models.Model):
    _name = "hrms.employee.position"
    _description = "Employee Position"

    name = fields.Char(related='employee_id.name', string='Employee Name', store=True, readonly=True)
    position_name = fields.Char(related='position_id.name', string='Position', readonly=True)
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Employee",
        required=True, index=True, copy=False,
        default=lambda self: self.env.context.get('employee_id.id', None)
    )
    position_id = fields.Many2one(
        comodel_name='hr.job',
        string="Position",
        required=True, index=True, copy=False
    )
    start_date = fields.Date(string="Appointment Date", required=True)
    end_date = fields.Date(string="Departure Date")
    departure_reason_id = fields.Many2one(
        comodel_name='hr.departure.reason',
        string="Departure Reason"
    )
    is_acting = fields.Boolean(string="Is Acting", default=False)
    appointment_letter = fields.Many2one(
        comodel_name="ir.attachment",
        string="Appointment Letter"
    )
    confirmation_letter = fields.Many2one(
        comodel_name="ir.attachment",
        string="Confirmation Letter"
    )

    _sql_constraints = [
        ('date_check', "CHECK ((start_date <= end_date OR end_date IS NULL))",
         "The start date must be anterior to the end date."),
    ]

    def open_record_departure_wizard(self):
        self.ensure_one()  # This will ensure the method is called on a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Record a Departure',
            'res_model': 'hrms.record.departure.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('hrms_core.view_hrms_record_departure_form').id,
            'target': 'new',
            'context':
                {
                    'employee_position_id': self.id,
                    'employee_id': self.employee_id.id,
                    'position_id': self.position_id.id
                },
        }





