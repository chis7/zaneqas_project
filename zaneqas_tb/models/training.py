from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date
from odoo import _, SUPERUSER_ID


class Training(models.Model):
    _name = 'training.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Training Management'

    name = fields.Char(string='Name of Training', required=True)
    type = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('online', 'Online'),
        ('distance', 'Distance Learning'),
        ('hybrid', 'Hybrid'),
    ], string='Type of Study', default='full_time', required=True)
    sponsor = fields.Selection([
        ('government', 'Government Sponsored'),
        ('self', 'Self Sponsored'),
        ('ngo', 'NGO Sponsored'),
        ('scholarship', 'Scholarship'),
    ], string='Sponsor', default='scholarship', required=True)
    sponsorship_type = fields.Selection([
        ('full', 'Full Sponsorship'),
        ('partial', 'Partial Sponsorship'),
        ('self', 'Self Sponsored'),
        ('other', 'Other'),
    ], string='Sponsorship Type', default='full', required=True)
    institution = fields.Char(string='Training Institution', required=True)
    #employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', default=lambda self: self._get_default_employee())

    country_id = fields.Many2one('res.country', string='Country', required=True)
    description = fields.Text(string='Reason to Pursue Course', required=True)
    description1 = fields.Text(string='Benefit to the Institution', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    duration = fields.Float(string='Duration', required=True)
    training_relevance = fields.Text(string='Relevance of Training')
    qualification = fields.Selection([
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('degree', 'Degree'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ], string='Qualification at the end of the Program', default='certificate', required=True)

    @api.depends('employee_id')
    def _compute_employee_type(self):
        for record in self:
            if record.employee_id:
                # Assuming the field name in 'hr.employee' is 'employee_type'
                # and it stores the selection value directly
                record.employee_type = record.employee_id.employee_type
            else:
                record.employee_type = None

    employee_type = fields.Char(compute='_compute_employee_type', string='Employee Type', store=True)

    supervisor_id = fields.Many2one('hr.employee', string="Supervisor", related='employee_id.parent_id', readonly=True)
    # supervisor_id = fields.Many2one('hr.employee', 'Supervisor', compute="_compute_supervisor_id", store=True,
    #                                 readonly=True,
    #                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    hod_comment = fields.Text(string='HOD Comment')
    bonding_date = fields.Date(string='Bonding Date')
    bonding_start_date = fields.Date(string='Bonding Start Date')
    bonding_end_date = fields.Date(string='Bonding End Date')
    rejection_comment = fields.Text(string='Rejection Comment')
    confirmation_status = fields.Text(string='Confirmation Status')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('supervisor_approved', 'Supervisor Approved'),
        ('hod_approved', 'HOD Approved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')

    @api.model
    def _get_default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    @api.depends('employee_id.parent_id')
    def _compute_supervisor_id(self):
        for record in self:
            record.supervisor_id = record.employee_id.parent_id

    # @api.depends('employee_id')
    # def _compute_approvals(self):
    #     for record in self:
    #         if record.employee_id:
    #             record.supervisor_id = record.employee_id.parent_id.user_id
    #             record.hod_id = record.employee_id.parent_id.parent_id.user_id if record.employee_id.parent_id else False
    #             record.ps_id = record.employee_id.parent_id.parent_id.parent_id.user_id if record.employee_id.parent_id.parent_id else False

    # def create(self, vals):
    #     res = super(Training, self).create(vals)
    #     return res


    def write(self, vals):
        res = super(Training, self).write(vals)
        return res


    def unlink(self):
        res = super(Training, self).unlink()
        return res


    def action_confirm(self):
        return self.write({'state': 'confirm'})


    def action_done(self):
        return self.write({'state': 'done'})


    def action_draft(self):
        return self.write({'state': 'draft'})

    def action_cancel(self):
        return self.write({'state': 'cancel'})


    def action_reject(self, comment=None):
        self.ensure_one()
    # Update the record with the rejection state and comment
        return self.write({'state': 'rejected', 'rejection_comment': comment})

    def action_supervisor_approve(self):
        if not self.supervisor_id.user_id or self.env.uid != self.supervisor_id.user_id.id:
            raise UserError(_('Only the Supervisor can approve at this stage.'))
        return self.write({'state': 'supervisor_approved'})

    # def action_supervisor_approve(self):
    #         raise UserError(_('The supervisor does not have a related user.'))
    #     # if self.state == 'confirm' and (self.env.uid == self.supervisor_id.id or self.env.uid == SUPERUSER_ID):
    #     if self.state == 'confirm' and self.employee_id.parent_id.id == self.supervisor_id.id:
    #         return self.write({'state': 'supervisor_approved'})
    #     else:
    #         raise UserError(_('Only the Supervisor can approve at this stage.'))

    def action_hod_approve(self):
        # Ensure the employee has a supervisor and the supervisor has a supervisor (HOD)
        if not self.employee_id.parent_id or not self.employee_id.parent_id.parent_id:
            raise UserError(_('The HOD cannot be determined.'))

        # Ensure the HOD has a related user
        hod = self.employee_id.parent_id.parent_id
        if not hod.user_id:
            raise UserError(_('The HOD does not have a related user.'))

        # Check if the current user is the HOD
        if self.env.uid != hod.user_id.id:
            raise UserError(_('Only the HOD can approve at this stage.'))

        # Approve the application
        return self.write({'state': 'hod_approved'})

    # def action_hod_approve(self):
    #     print("Employee ID: ", self.employee_id.id)
    #     print("Supervisor ID: ", self.supervisor_id.id)
    #     print("Current User ID: ", self.env.uid)
    #     print("Supervisor ID222: ", self.employee_id.parent_id.id)
    #     if self.state == 'supervisor_approved' and (self.employee_id.parent_id.id == self.supervisor_id.id):
    #         return self.write({'state': 'hod_approved'})
    #     else:
    #         raise UserError(_('Only the HOD can approve at this stage.'))

    def action_ps_approve(self):
        # Ensure the employee has a HOD and the HOD has a PS
        if not self.employee_id.parent_id or not self.employee_id.parent_id.parent_id or not self.employee_id.parent_id.parent_id.parent_id:
            raise UserError(_('The PS cannot be determined.'))

        # Ensure the Director has a related user
        director = self.employee_id.parent_id.parent_id.parent_id
        if not director.user_id:
            raise UserError(_('The PS does not have a related user.'))

        # Check if the current user is the PS
        if self.env.uid != director.user_id.id:
            raise UserError(_('Only the PS can approve at this stage.'))

        # Approve the application
        return self.write({'state': 'approved'})

        @api.constrains('start_date', 'end_date', 'bonding_date', 'bonding_start_date', 'bonding_end_date')
        def _check_date_fields(self):
            for record in self:
                today = fields.Date.today()
                if record.start_date and record.start_date < today:
                    raise ValidationError("The start date cannot be in the past. Please select today's date or a future date.")
                if record.end_date and (record.end_date < record.start_date or record.end_date < today):
                    raise ValidationError("The end date cannot be before the start date or in the past.")
                if record.bonding_date and record.bonding_date < today:
                    raise ValidationError("The bonding date cannot be in the past.")
                if record.bonding_start_date and record.bonding_start_date < today:
                    raise ValidationError("The bonding start date cannot be in the past.")
                if record.bonding_end_date and (record.bonding_end_date < record.bonding_start_date or record.bonding_end_date < today):
                    raise ValidationError("The bonding end date cannot be before the bonding start date or in the past.")

        # if self.state == 'hod_approved' and (self.employee_id.parent_id.id == self.supervisor_id.id):
        #     return self.write({'state': 'approved'})
        # else:
        #     raise UserError(_('Only the PS can approve at this stage.'))

