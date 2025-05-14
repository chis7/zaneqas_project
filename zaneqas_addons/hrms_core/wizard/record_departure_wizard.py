# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
###############################################################################

from odoo import models, fields, api


class RecordDepartureWizard(models.TransientModel):
    _name = "hrms.record.departure.wizard"
    _description = "Record Departure Wizard"

    employee_position_id = fields.Many2one(
        comodel_name='hrms.employee.position', string='Employee Position', required=True,
        default=lambda self: self.env.context.get('employee_position_id', None)
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Employee', required=True,
        default=lambda self: self.env.context.get('employee_id', None)
    )
    position_id = fields.Many2one(
        comodel_name='hr.job', string='Position', required=True,
        default=lambda self: self.env.context.get('position_id', None),
    )
    departure_date = fields.Date(string="Departure Date")
    departure_reason_id = fields.Many2one(
        comodel_name='hr.departure.reason',
        string="Departure Reason"
    )

    def action_record_departure(self):
        self.employee_position_id.write({'departure_reason_id': self.departure_reason_id})
        self.employee_position_id.write({'end_date': self.departure_date})

