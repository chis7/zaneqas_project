# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # last_name = fields.Char(string='Last Name', required=True, tracking=True)
    # first_name = fields.Char(string='First Name', required=True, tracking=True)
    # other_names = fields.Char(string='Other Names', tracking=True)
    mpsa_file_number = fields.Char(string="MPSA File Number", tracking=True)
    employee_number = fields.Char(string='Employee Number', tracking=True)
    psmd_file_number = fields.Char(string="PSMD File Number", tracking=True)
    date_of_first_appointment = fields.Date(string='Date First Appointment', compute='_compute_date_of_first_appointment')
    date_of_present_appointment = fields.Date(string="Date To Present Appointment", compute='_compute_date_of_present_appointment')
    current_job_id = fields.Char(string='Current Job ID', compute='_compute_current_job_id')
    marital_status = fields.Selection(
        selection=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('divorced', 'Divorced')],
        string='Marital Status',
        tracking=True)
    qualification_lines = fields.One2many(
        comodel_name='hrms.qualification.line',
        inverse_name='employee_id',
        string="Qualifications",
        copy=True, auto_join=True)
    # competency_lines = fields.One2many(
    #     comodel_name='hrms.competency.line',
    #     string="Competencies"
    # )

    # @api.onchange('last_name', 'first_name')
    # def _compute_name(self):
    #     for record in self:
    #         record.name = ' '.join([record.first_name or '', record.last_name or ''])

    @api.onchange('date_of_first_appointment')
    def _compute_date_of_first_appointment(self):
        for record in self:
            record.date_of_first_appointment = self.date_of_first_appointment

    @api.onchange('date_of_present_appointment')
    def _compute_date_of_present_appointment(self):
        for record in self:
            record.date_of_present_appointment = self.date_of_present_appointment

    @api.onchange('current_job_id')
    def _compute_current_job_id(self):
        for record in self:
            record.current_job_id = self.current_job_id
