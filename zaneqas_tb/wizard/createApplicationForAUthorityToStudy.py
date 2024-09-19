# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models, _, api


class CreateTrainingPlanWizardLines(models.TransientModel):
    _name = "create.training.plan.wizard.lines"
    _description = "training plan lines wizard"

    employee_id = fields.Many2one('hr.employee', string="Candidate Name", required=True, store=True)
    priorityRanking = fields.Integer(string="Priority Ranking", required=True, store=True)
    priorityArea = fields.Char(string="Priority Area", required=True, store=True)

    name = fields.Char(string="Training Proposed", required=True, store=True)
    level_of_training_proposed = fields.Char(string="Level of Training Proposed", required=True, store=True)
    location_of_programme_proposed = fields.Many2one("res.country", "Location of Programme Proposed", required=True,
                                                     store=True)
    proposed_date_of_programme = fields.Date(string="Proposed Date of Programme", required=True, store=True)
    sponsor_id = fields.Many2one('training.sponsor', string="Sponsor", required=True, store=True)
    justification_of_training = fields.Text(string="Justification of Training", required=True, store=True)
    estimated_cost_per_year = fields.Integer(string="Estimated Cost per Year", required=True, store=True)
    institution = fields.Many2one('training.training.institution', string='Training Institution', store=True)
    start_date = fields.Date(string='Start Date', store=True)
    end_date = fields.Date(string='End Date', store=True)
    duration = fields.Float(string='Duration', store=True)
    state = fields.Selection([
        ('not_applied', 'Started But Not Applied'),
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('supervisor_approved', 'Supervisor Approved'),
        ('hod_approved', 'HOD Approved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='not_applied', store=True)
    training_plan_id = fields.Many2one('training.plan', string="Training Plan", store=True)
    training_plan_state = fields.Selection(
        related='training_plan_id.state',
        string="Training Plan State",
        readonly=True,
        store=True
    )
    is_current_user_employee = fields.Boolean(compute='_compute_is_current_user_employee', store=False)

    def save_application_for_authority_to_study(self):
        self.ensure_one()  # Ensure that the method is called on a single record
        training_plan_lines = self.env['training.plan.lines'].search(
            [('training_plan_id', '=', self.training_plan_id.id)])
        if training_plan_lines:
            for line in training_plan_lines:
                if line.employee_id.user_id.id == self.env.uid and line.state == 'not_applied':
                    line.write({
                        'institution': self.institution.id,
                        'start_date': self.start_date,
                        'end_date': self.end_date,
                        'duration': self.duration,
                        'state': 'draft'
                    })
                else:
                    pass
        return True
