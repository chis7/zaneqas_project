# -*- coding: utf-8 -*-
import time
from datetime import datetime, date

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class CreateTrainingPlanWizardLines(models.TransientModel):
    _name = "create.trainee.post.training.evaluation.wizard.lines"
    _description = "trainee post training evaluation lines wizard"

    self_evaluation_extent_objectives_achieved = fields.Selection(
        selection=[
            ("extent_objectives_achieved_1", "1"),
            ("extent_objectives_achieved_2", "2"),
            ("extent_objectives_achieved_3", "3"),
            ("extent_objectives_achieved_4", "4"),
            ("extent_objectives_achieved_5", "5"),
        ],
        string="To what extent were you able to achieve objectives / targets as shown in the Departmental/Unit Work Plans before the training?",
        tracking=True,
    )
    self_evaluation_extent_training_helped = fields.Selection(
        selection=[
            ("extent_training_helped_1", "1"),
            ("extent_training_helped_2", "2"),
            ("extent_training_helped_3", "3"),
            ("extent_training_helped_4", "4"),
            ("extent_training_helped_5", "5"),
        ],
        string="To what extent has the training helped you in achieving objectives and targets as stated in your Departmental/Unit Work Plans?",
        tracking=True,
    )
    self_evaluation_performance_rating_before = fields.Selection(
        selection=[
            ("performance_rating_before_1", "1"),
            ("performance_rating_before_2", "2"),
            ("performance_rating_before_3", "3"),
            ("performance_rating_before_4", "4"),
            ("performance_rating_before_5", "5"),
        ],
        string="How do you rate your job performance before the training?", tracking=True,
    )

    self_evaluation_performance_rating_current = fields.Selection(
        selection=[
            ("performance_rating_current_1", "1"),
            ("performance_rating_current_2", "2"),
            ("performance_rating_current_3", "3"),
            ("performance_rating_current_4", "4"),
            ("performance_rating_current_5", "5"),
        ],
        string="How do you rate your job performance now?", tracking=True,
    )

    self_evaluation_able_to_apply_knowledge = fields.Boolean(
        string="Are you able to apply the Knowledge, Skills and Attitude acquired from the training to your job",
        default=False, )

    self_evaluation_hindering_factors_lack_of_understanding = fields.Boolean(
        string="Lack of understanding from your subordinates and /or colleagues",
        default=False, )
    self_evaluation_hindering_factors_supervisor_priorities_other = fields.Boolean(
        string="Supervising Officer has other priorities",
        default=False, )
    self_evaluation_hindering_factors_constant_changes = fields.Boolean(
        string="Constant changes within the Ministry/Province/Institution",
        default=False, )
    self_evaluation_hindering_factors_processes_not_flexible = fields.Boolean(
        string="The systems, procedures and work processes are not flexible enough",
        default=False, )
    self_evaluation_hindering_factors_unclear_responsibilities = fields.Boolean(
        string="Levels of authority and responsibilities are not clear",
        default=False, )
    self_evaluation_hindering_factors_not_enough_time = fields.Boolean(string="Not enough time due to pressure of work",
                                                                       default=False, )
    self_evaluation_hindering_factors_not_relevant_to_current_job = fields.Boolean(
        string="Learning content of the course was not relevant to current job",
        default=False, )
    self_evaluation_hindering_factors_unclear_work_plans = fields.Boolean(
        string="Departmental/Unit Work Plans are not clear and specific",
        default=False, )
    self_evaluation_hindering_factors_lack_of_resources = fields.Boolean(string="Lack of resources", default=False, )
    self_evaluation_hindering_factors_other = fields.Text(string="Others, (Specify)",
                                                          default=False, )

    self_evaluation_lack_of_resources_finances = fields.Boolean(string="Finances", default=False, )
    self_evaluation_lack_of_resources_equipment = fields.Boolean(string="Equipment", default=False, )
    self_evaluation_lack_of_resources_human_resource = fields.Boolean(string="Human Resource", default=False, )
    self_evaluation_lack_of_resources_information_technology = fields.Boolean(string="Information Technology",
                                                                              default=False, )
    self_evaluation_lack_of_resources_other = fields.Boolean(string="Others, (Specify)", default=False, )

    self_evaluation_factors_to_enhance_learning_more_training = fields.Boolean(string="More training", default=False, )
    self_evaluation_factors_to_enhance_learning_right_job_placement = fields.Boolean(
        string="Being placed in the right job",
        default=False, )
    self_evaluation_factors_to_enhance_learning_more_time = fields.Boolean(
        string="More time to practice the acquired knowledge and skills", default=False, )
    self_evaluation_factors_to_enhance_learning_supervisor_Support = fields.Boolean(
        string="Support from my Supervising Officer",
        default=False, )
    self_evaluation_factors_to_enhance_learning_modern_equipment = fields.Boolean(string="Modern Equipment",
                                                                                  default=False, )
    self_evaluation_factors_to_enhance_learning_others = fields.Boolean(string="Others, (specify)", default=False, )

    self_evaluation_extent_assisted_staff_subordinates = fields.Selection(
        selection=[
            ("extent_assisted_staff_subordinates_1", "1"),
            ("extent_assisted_staff_subordinates_2", "2"),
            ("extent_assisted_staff_subordinates_3", "3"),
            ("extent_assisted_staff_subordinates_4", "4"),
            ("extent_assisted_staff_subordinates_5", "5"),
        ],
        string="Your subordinates", tracking=True,
    )

    self_evaluation_extent_assisted_staff_supervisor = fields.Selection(
        selection=[
            ("extent_assisted_staff_supervisor_1", "1"),
            ("extent_assisted_staff_supervisor_2", "2"),
            ("extent_assisted_staff_supervisor_3", "3"),
            ("extent_assisted_staff_supervisor_4", "4"),
            ("extent_assisted_staff_supervisor_5", "5"),
        ],
        string="Your Supervisor", tracking=True,
    )

    self_evaluation_extent_assisted_staff_colleagues = fields.Selection(
        selection=[
            ("extent_assisted_staff_colleagues_1", "1"),
            ("extent_assisted_staff_colleagues_2", "2"),
            ("extent_assisted_staff_colleagues_3", "3"),
            ("extent_assisted_staff_colleagues_4", "4"),
            ("extent_assisted_staff_colleagues_5", "5"),
        ],
        string="Your colleagues", tracking=True,
    )

    self_evaluation_comments_other = fields.Text(string="Others, specify")

    self_evaluation_facility_rating_other = fields.Text(
        string="Please add any other comments that feel would improve the course.")
    state = fields.Selection([
        ('not_applied', 'Not Applied'),
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('supervisor', 'Supervisor'),
        ('hod', 'HOD'),
        ('ps', 'PS'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
        ('bonded', 'Bonded'),
        ('training_in_progress', 'Training In-progress'),
        ('training_completed', 'Training Completed'),
        ('training_self_evaluation_evaluated', 'Training Self Evaluated'),
        ('training_supervisor_evaluated', 'Training Supervisor Evaluated'),
    ], string='Status', default='not_applied', store=True, tracking=True)
    training_plan_id = fields.Many2one('training.plan', string="Training Plan", store=True)
    training_plan_state = fields.Selection(
        related='training_plan_id.state',
        string="Training Plan State",
        readonly=True,
        store=True
    )

    def action_save_evaluation_as_draft(self):
        self.write({'state': 'training_self_evaluation_evaluated'})

    def action_submit_evaluation(self):
        self.write({'state': 'training_supervisor_evaluated'})

    def save_trainee_post_training_evaluation(self):
        self.ensure_one()  # Ensure that the method is called on a single record
        # training_plan_line = self.env['training.plan.lines'].browse(self.training_plan_id.id)
        training_plan_lines = self.env['training.plan.lines'].search(
            [('training_plan_id', '=', self.training_plan_id.id)])

        if training_plan_lines:
            today = date.today()
            for line in training_plan_lines:
                if line.employee_id.user_id.id == self.env.uid and line.state == 'training_completed':
                    line.write({
                        'self_evaluation_extent_objectives_achieved': self.self_evaluation_extent_objectives_achieved,
                        'self_evaluation_extent_training_helped': self.self_evaluation_extent_training_helped,
                        'self_evaluation_performance_rating_before': self.self_evaluation_performance_rating_before,
                        'self_evaluation_performance_rating_current': self.self_evaluation_performance_rating_current,
                        'self_evaluation_able_to_apply_knowledge': self.self_evaluation_able_to_apply_knowledge,
                        'self_evaluation_hindering_factors_lack_of_understanding': self.self_evaluation_hindering_factors_lack_of_understanding,
                        'self_evaluation_hindering_factors_supervisor_priorities_other': self.self_evaluation_hindering_factors_supervisor_priorities_other,
                        'self_evaluation_hindering_factors_constant_changes': self.self_evaluation_hindering_factors_constant_changes,
                        'self_evaluation_hindering_factors_processes_not_flexible': self.self_evaluation_hindering_factors_processes_not_flexible,
                        'self_evaluation_hindering_factors_unclear_responsibilities': self.self_evaluation_hindering_factors_unclear_responsibilities,
                        'self_evaluation_hindering_factors_not_enough_time': self.self_evaluation_hindering_factors_not_enough_time,
                        'self_evaluation_hindering_factors_not_relevant_to_current_job': self.self_evaluation_hindering_factors_not_relevant_to_current_job,
                        'self_evaluation_hindering_factors_unclear_work_plans': self.self_evaluation_hindering_factors_unclear_work_plans,
                        'self_evaluation_hindering_factors_lack_of_resources': self.self_evaluation_hindering_factors_lack_of_resources,
                        'self_evaluation_hindering_factors_other': self.self_evaluation_hindering_factors_other,
                        'self_evaluation_lack_of_resources_finances': self.self_evaluation_lack_of_resources_finances,
                        'self_evaluation_lack_of_resources_equipment': self.self_evaluation_lack_of_resources_equipment,
                        'self_evaluation_lack_of_resources_human_resource': self.self_evaluation_lack_of_resources_human_resource,
                        'self_evaluation_lack_of_resources_information_technology': self.self_evaluation_lack_of_resources_information_technology,
                        'self_evaluation_lack_of_resources_other': self.self_evaluation_lack_of_resources_other,
                        'self_evaluation_factors_to_enhance_learning_more_training': self.self_evaluation_factors_to_enhance_learning_more_training,
                        'self_evaluation_factors_to_enhance_learning_right_job_placement': self.self_evaluation_factors_to_enhance_learning_right_job_placement,
                        'self_evaluation_factors_to_enhance_learning_more_time': self.self_evaluation_factors_to_enhance_learning_more_time,
                        'self_evaluation_factors_to_enhance_learning_supervisor_Support': self.self_evaluation_factors_to_enhance_learning_supervisor_Support,
                        'self_evaluation_factors_to_enhance_learning_modern_equipment': self.self_evaluation_factors_to_enhance_learning_modern_equipment,
                        'self_evaluation_factors_to_enhance_learning_others': self.self_evaluation_factors_to_enhance_learning_others,
                        'self_evaluation_extent_assisted_staff_subordinates': self.self_evaluation_extent_assisted_staff_subordinates,
                        'self_evaluation_extent_assisted_staff_supervisor': self.self_evaluation_extent_assisted_staff_supervisor,
                        'self_evaluation_extent_assisted_staff_colleagues': self.self_evaluation_extent_assisted_staff_colleagues,
                        'self_evaluation_comments_other': self.self_evaluation_comments_other,
                        'self_evaluation_facility_rating_other': self.self_evaluation_facility_rating_other,
                        'self_evaluation_date': today.strftime('%Y-%m-%d'),
                        'state': 'training_self_evaluation_evaluated'
                        })
                else:
                    pass
        return True