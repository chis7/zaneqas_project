from odoo import models, fields, api
from datetime import datetime


class DepartmentalObjective(models.Model):
    _name = 'hrms.departmental.objective'
    _description = 'Departmental Objectives'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    department_id = fields.Many2one('hr.department', string='Department')
    # work_plan_id = fields.Many2one('hrms.departmental.work.plan', string='Work Plan', ondelete='cascade')
    # activities = fields.One2many('hrms.departmental.work.plan.activity', 'objective_id', string='Activities')

class DepartmentalWorkPlanActivity(models.Model):
    _name = 'hrms.departmental.work.plan.activity'
    _description = 'Departmental Work Plan Activity'
    _rec_name = 'sequence'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(
        string='Reference',
        required=True, copy=False, readonly=True, index=True,
        default=lambda self: ('New'))
    description = fields.Text(string='Description')
    work_plan_id = fields.Many2one('hrms.departmental.work.plan', string='Work Plan', ondelete='cascade')
    objective_id = fields.Many2one('hrms.departmental.objective', string='Objective')
    responsible_id = fields.Many2one('hr.employee', string='Responsible')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Status', default='not_started')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', ('New')) == ('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hrms.departmental.work.plan.activity') or ('New')
            result = super(DepartmentalWorkPlanActivity, self).create(vals)
            return result

class DepartmentalWorkPlan(models.Model):
    _name = 'hrms.departmental.work.plan'
    _description = 'Departmental Work Plan'
    _rec_name = 'sequence'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(
        string='Reference',
        required=True, copy=False, readonly=True, index=True,
        default=lambda self: ('New'))
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    department_id = fields.Many2one('hr.department', string='Department')
    activity_ids = fields.One2many('hrms.departmental.work.plan.activity', 'work_plan_id', string='Activities')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], string='Status', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', ('New')) == ('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hrms.departmental.work.plan') or ('New')
            result = super(DepartmentalWorkPlan, self).create(vals_list)
            return result


