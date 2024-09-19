from odoo import models, fields, api
from datetime import datetime


class StrategicPlan(models.Model):
    _name = 'hrms.strategic.plan'
    _description = 'Strategic Plan'

    sequence = fields.Char(
        string='Reference',
        required=True, copy=False, readonly=True, index=True,
        default=lambda self: 'New')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    objectives = fields.One2many(
        comodel_name='hrms.strategic.plan.objective',
        inverse_name='plan_id',
        string='Objectives')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hrms.strategic.plan') or ('New')
            result = super(StrategicPlan, self).create(vals_list)
            return result


class StrategicPlanObjective(models.Model):
    _name = 'hrms.strategic.plan.objective'
    _description = 'Strategic Plan Objective'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    plan_id = fields.Many2one('hrms.strategic.plan', string='Strategic Plan', ondelete='cascade')
    initiatives = fields.One2many('hrms.strategic.plan.initiative', 'objective_id', string='Initiatives')


class StrategicPlanInitiative(models.Model):
    _name = 'hrms.strategic.plan.initiative'
    _description = 'Strategic Plan Initiative'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    objective_id = fields.Many2one('hrms.strategic.plan.objective', string='Objective', ondelete='cascade')
    responsible_id = fields.Many2one('hr.employee', string='Responsible')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    budget = fields.Float(string='Budget')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string='Status', default='draft')
