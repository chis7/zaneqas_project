# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    last_name = fields.Char(string='Last Name', tracking=True)
    first_name = fields.Char(string='First Name', tracking=True)
    other_names = fields.Char(string='Other Names', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    institution_file_number = fields.Char(string="Institution File Number", tracking=True)
    employee_number = fields.Char(string='Employee Number', tracking=True)
    psmd_file_number = fields.Char(string="PSMD File Number", tracking=True)
    date_of_first_appointment = fields.Date(string='Date of First Appointment', compute='_compute_date_of_first_appointment')
    date_of_present_appointment = fields.Date(string="Date of Present Appointment", compute='_compute_date_of_present_appointment')
    marital_status = fields.Selection(
        selection=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('divorced', 'Divorced')],
        string='Marital Status',
        tracking=True
    )
    qualifications = fields.One2many(
        comodel_name='hrms.employee.qualification',
        inverse_name='employee_id',
        string="Qualifications",
        copy=True, auto_join=True
    )
    position_ids = fields.One2many(
        comodel_name='hrms.employee.position',
        inverse_name='employee_id',
        string="Positions"
    )
    position_count = fields.Integer(compute="_compute_position_count")
    license_count = fields.Integer(compute="_compute_license_count")
    current_position_id = fields.Many2one(
        comodel_name='hr.job',
        compute='_compute_current_position_id',
        store=True
    )
    current_position_title = fields.Char(
        string="Position",
        compute='_compute_current_position_title',
        store=True
    )
    years_in_service = fields.Integer(string="Years in Service", compute="_compute_years_in_service", store=True)


    @api.depends('last_name', 'first_name', 'other_names')
    def _compute_name(self):
        for employee in self:
            first = employee.first_name or ''
            last = employee.last_name or ''
            other = employee.other_names or ''
            # Concatenate first name, other names and last name, ensuring proper formatting
            employee.name = f"{first} {other} {last}".strip()

    @api.onchange('last_name', 'first_name', 'other_names')
    def onchange_name(self):
        first = self.first_name or ''
        last = self.last_name or ''
        other = self.other_names or ''
        # Concatenate first name, other names and last name, ensuring proper formatting
        self.name = f"{first} {other} {last}".strip()

    @api.model
    def create(self, vals):
        first = vals.get('first_name') or ''
        last = vals.get('last_name') or ''
        other = vals.get('other_names') or ''
        vals['name'] = f"{first} {other} {last}".strip()
        self.resource_id.name = f"{first} {other} {last}".strip()
        result = super(HrEmployee, self).create(vals)
        return result

    @api.depends('birthday')
    def _compute_age(self):
        for employee in self:
            if employee.birthday:
                today = date.today()
                birthdate = fields.Date.from_string(employee.birthday)
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                employee.age = age
            else:
                employee.age = 0

    # @api.onchange('birthday')
    # def onchange_birthday(self):
    #     for employee in self:
    #         if employee.birthday:
    #             today = date.today()
    #             birthdate = fields.Date.from_string(employee.birthday)
    #             age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    #             employee.age = age
    #         else:
    #             employee.age = 0

    @api.depends('position_ids.start_date')
    def _compute_date_of_first_appointment(self):
        for employee in self:
            first_position = self.env['hrms.employee.position'].search([
                ('employee_id', '=', employee.id)
            ], order='start_date asc', limit=1)
            employee.date_of_first_appointment = first_position.start_date if first_position else False

    @api.depends('position_ids.start_date')
    def _compute_date_of_present_appointment(self):
        for employee in self:
            latest_position = self.env['hrms.employee.position'].search([
                ('employee_id', '=', employee.id)
            ], order='start_date desc', limit=1)
            employee.date_of_present_appointment = latest_position.start_date if latest_position else False

    def _compute_position_count(self):
        all_positions = self.env['hrms.employee.position'].read_group([
            ('employee_id', 'in', self.ids),
        ], fields=['employee_id'], groupby=['employee_id'])

        mapping = dict([(case['employee_id'][0], case['employee_id_count']) for case in all_positions])

        for employee in self:
            employee.position_count = mapping.get(employee.id, 0)

    def _compute_license_count(self):
        all_licenses = self.env['hrms.employee.license'].read_group([
            ('employee_id', 'in', self.ids),
        ], fields=['employee_id'], groupby=['employee_id'])

        mapping = dict([(case['employee_id'][0], case['employee_id_count']) for case in all_licenses])

        for employee in self:
            employee.license_count = mapping.get(employee.id, 0)

    @api.depends('position_ids')
    def _compute_current_position_id(self):
        for employee in self:
            current_position = self.env['hrms.employee.position'].search([
                ('employee_id', '=', employee.id),
                ('end_date', '=', False)
            ], limit=1)
            employee.current_position_id = current_position.position_id if current_position else None

    @api.depends('current_position_id')
    def _compute_current_position_title(self):
        for employee in self.filtered('current_position_id'):
            employee.current_position_title = employee.current_position_id.name

    @api.depends('date_of_first_appointment')
    def _compute_years_in_service(self):
        """Calculates the years in service by finding the difference between the current date and the date of first appointment."""
        today = date.today()
        for employee in self:
            if employee.date_of_first_appointment:
                first_appointment_date = fields.Date.from_string(employee.date_of_first_appointment)
                years = today.year - first_appointment_date.year - (
                        (today.month, today.day) < (first_appointment_date.month, first_appointment_date.day))
                employee.years_in_service = years
            else:
                employee.years_in_service = 0

    def action_open_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'type': 'ir.actions.act_window',
            'res_model': 'hrms.employee.document',
            'view_mode': 'kanban,tree,form',
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
                'default_company_id': self.company_id.id,
            },
            'domain': [('res_id', 'in', self.ids), ('res_model', '=', self._name)],
            'target': 'current',
            'help': """
                <p class="o_view_nocontent_smiling_face">
                    %s
                </p><p>
                    %s
                    <br/>
                    %s
                </p>
            """ % (
                _("Upload files to employee"),
                _("Use this feature to store any files you would like to share with your customers."),
                _("E.g: Arrival Advice and other documents not captured in other places in the system, ..."),
                _("Please note: Documents relating to qualifications should be not be uploaded here but under qualification section on the emloyee record"),
            )
        }
