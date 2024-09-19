# -*- coding: utf-8 -*-
import time
from datetime import datetime, date

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class CreateSupervisorTrainingPlanWizardLines(models.TransientModel):
    _name = "create.supervisor.post.training.evaluation.wizard.lines"
    _description = "supervisor post training evaluation lines wizard"

    supervisor_evaluation_extent_objectives_achieved_before = fields.Selection(
        selection=[
            ("extent_objectives_achieved_before_1", "1"),
            ("extent_objectives_achieved_before_2", "2"),
            ("extent_objectives_achieved_before_3", "3"),
            ("extent_objectives_achieved_before_4", "4"),
            ("extent_objectives_achieved_before_5", "5"),
        ],
        string="To what extent has the trainee been able to achieve the objectives/targets shown in the Departmental/Unit Work Plans before the training?",
        tracking=True,
    )

    supervisor_evaluation_extent_objectives_achieved_after = fields.Selection(
        selection=[
            ("extent_objectives_achieved_after_1", "1"),
            ("extent_objectives_achieved_after_2", "2"),
            ("extent_objectives_achieved_after_3", "3"),
            ("extent_objectives_achieved_after_4", "4"),
            ("extent_objectives_achieved_after_5", "5"),
        ],
        string="To what extent was the trainee able to achieve the objectives and targets stated in your Departmental/Unit Work plans after the training?",
        tracking=True,
    )
    supervisor_evaluation_extent_training_helped = fields.Selection(
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
    supervisor_evaluation_performance_rating_before = fields.Selection(
        selection=[
            ("performance_rating_before_1", "1"),
            ("performance_rating_before_2", "2"),
            ("performance_rating_before_3", "3"),
            ("performance_rating_before_4", "4"),
            ("performance_rating_before_5", "5"),
        ],
        string="To what extent do you think this training has impacted on the trainee’s job performance?",
        tracking=True,
    )

    supervisor_evaluation_performance_rating_current = fields.Selection(
        selection=[
            ("performance_rating_current_1", "1"),
            ("performance_rating_current_2", "2"),
            ("performance_rating_current_3", "3"),
            ("performance_rating_current_4", "4"),
            ("performance_rating_current_5", "5"),
        ],
        string="How do you rate your job performance now?", tracking=True,
    )

    supervisor_evaluation_able_to_apply_knowledge = fields.Boolean(
        string="Has the trainee been able to apply knowledge, skills and attitudes acquired from the course to his/her job?",
        default=False,
        required=True)

    supervisor_evaluation_hindering_factors_lack_of_understanding = fields.Boolean(
        string="Lack of understanding from his/her subordinates and/or colleagues",
        default=False, required=True)
    # supervisor_evaluation_hindering_factors_supervisor_priorities_other = fields.Boolean(
    #     string="You have other priorities",
    #     default=False, required=True)
    supervisor_evaluation_hindering_factors_constant_changes = fields.Boolean(
        string="Constant changes within the Ministry/Province/Institution",
        default=False, required=True)
    supervisor_evaluation_hindering_factors_processes_not_flexible = fields.Boolean(
        string="The systems, procedures and work processes are not flexible enough",
        default=False, required=True)
    # supervisor_evaluation_hindering_factors_unclear_responsibilities = fields.Boolean(
    #     string="Levels of authority and responsibilities are not clear",
    #     default=False, required=True)
    supervisor_evaluation_hindering_factors_not_enough_time = fields.Boolean(
        string="Not enough time due to pressure of work",
        default=False, required=True)
    # supervisor_evaluation_hindering_factors_not_relevant_to_current_job = fields.Boolean(
    #     string="Learning content of the course was not relevant to current job",
    #     default=False, required=True)
    supervisor_evaluation_hindering_factors_unclear_work_plans = fields.Boolean(
        string="Departmental/Unit Work Plans are not clear and specific",
        default=False, required=True)
    supervisor_evaluation_hindering_factors_lack_of_resources = fields.Boolean(string="Lack of resources",
                                                                               default=False, required=True)
    supervisor_evaluation_hindering_factors_other = fields.Boolean(string="Others, (Specify)",
                                                                   default=False, required=True)

    supervisor_evaluation_lack_of_resources_finances = fields.Boolean(string="Finances", default=False, required=True)
    supervisor_evaluation_lack_of_resources_equipment = fields.Boolean(string="Equipment", default=False, required=True)
    supervisor_evaluation_lack_of_resources_human_resource = fields.Boolean(string="Human Resource", default=False,
                                                                            required=True)
    supervisor_evaluation_lack_of_resources_information_technology = fields.Boolean(string="Information Technology",
                                                                                    default=False,
                                                                                    required=True)
    supervisor_evaluation_lack_of_resources_other = fields.Boolean(string="Others, (Specify)", default=False,
                                                                   required=True)

    supervisor_evaluation_factors_to_enhance_learning_more_training = fields.Boolean(string="More training",
                                                                                     default=False, required=True)
    # supervisor_evaluation_factors_to_enhance_learning_right_job_placement = fields.Boolean(
    #     string="Being placed in the right job",
    #     default=False, required=True)
    supervisor_evaluation_factors_to_enhance_learning_more_time = fields.Boolean(
        string="More time to practice the acquired knowledge and skills", default=False, required=True)
    # supervisor_evaluation_factors_to_enhance_learning_supervisor_Support = fields.Boolean(
    #     string="Support from my Supervising Officer",
    #     default=False, required=True)
    # supervisor_evaluation_factors_to_enhance_learning_modern_equipment = fields.Boolean(string="Modern Equipment",
    #                                                                                     default=False,
    #                                                                                     required=True)
    supervisor_evaluation_factors_to_enhance_learning_others = fields.Boolean(string="Others, (specify)", default=False,
                                                                              required=True)

    supervisor_evaluation_extent_assisted_staff_subordinates = fields.Selection(
        selection=[
            ("extent_assisted_staff_subordinates_1", "1"),
            ("extent_assisted_staff_subordinates_2", "2"),
            ("extent_assisted_staff_subordinates_3", "3"),
            ("extent_assisted_staff_subordinates_4", "4"),
            ("extent_assisted_staff_subordinates_5", "5"),
        ],
        string="Your subordinates", tracking=True,
    )

    supervisor_evaluation_extent_assisted_staff_supervisor = fields.Selection(
        selection=[
            ("extent_assisted_staff_supervisor_1", "1"),
            ("extent_assisted_staff_supervisor_2", "2"),
            ("extent_assisted_staff_supervisor_3", "3"),
            ("extent_assisted_staff_supervisor_4", "4"),
            ("extent_assisted_staff_supervisor_5", "5"),
        ],
        string="Your Supervisor", tracking=True,
    )

    supervisor_evaluation_extent_assisted_staff_colleagues = fields.Selection(
        selection=[
            ("extent_assisted_staff_colleagues_1", "1"),
            ("extent_assisted_staff_colleagues_2", "2"),
            ("extent_assisted_staff_colleagues_3", "3"),
            ("extent_assisted_staff_colleagues_4", "4"),
            ("extent_assisted_staff_colleagues_5", "5"),
        ],
        string="Your colleagues", tracking=True,
    )

    supervisor_evaluation_usefulness_other = fields.Char(string="Others, specify", required=False)

    supervisor_evaluation_facility_rating_other = fields.Text(
        string="Please add any other comments that feel would improve the course.",
        required=False)
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
        self.write({'state': 'training_supervisor_evaluated'})

    def action_submit_evaluation(self):
        self.write({'state': 'training_supervisor_evaluated'})

    def save_supervisor_post_training_evaluation(self):
        self.ensure_one()  # Ensure that the method is called on a single record
        training_plan_lines = self.env['training.plan.lines'].search(
            [('training_plan_id', '=', self.training_plan_id.id)])
        if training_plan_lines:
            today = date.today()
            for line in training_plan_lines:

                if self.env.user == line.employee_id.parent_id.user_id and line.state == 'training_self_evaluation_evaluated':
                    line.write({
                        'supervisor_evaluation_extent_objectives_achieved_before': self.supervisor_evaluation_extent_objectives_achieved_before,
                        'supervisor_evaluation_extent_objectives_achieved_after': self.supervisor_evaluation_extent_objectives_achieved_after,
                        'supervisor_evaluation_extent_training_helped': self.supervisor_evaluation_extent_training_helped,
                        'supervisor_evaluation_performance_rating_before': self.supervisor_evaluation_performance_rating_before,
                        'supervisor_evaluation_performance_rating_current': self.supervisor_evaluation_performance_rating_current,
                        'supervisor_evaluation_able_to_apply_knowledge': self.supervisor_evaluation_able_to_apply_knowledge,
                        'supervisor_evaluation_hindering_factors_lack_of_understanding': self.supervisor_evaluation_hindering_factors_lack_of_understanding,
                        'supervisor_evaluation_hindering_factors_constant_changes': self.supervisor_evaluation_hindering_factors_constant_changes,
                        'supervisor_evaluation_hindering_factors_processes_not_flexible': self.supervisor_evaluation_hindering_factors_processes_not_flexible,
                        'supervisor_evaluation_hindering_factors_not_enough_time': self.supervisor_evaluation_hindering_factors_not_enough_time,
                        'supervisor_evaluation_hindering_factors_unclear_work_plans': self.supervisor_evaluation_hindering_factors_unclear_work_plans,
                        'supervisor_evaluation_hindering_factors_lack_of_resources': self.supervisor_evaluation_hindering_factors_lack_of_resources,
                        'supervisor_evaluation_hindering_factors_other': self.supervisor_evaluation_hindering_factors_other,
                        'supervisor_evaluation_lack_of_resources_finances': self.supervisor_evaluation_lack_of_resources_finances,
                        'supervisor_evaluation_lack_of_resources_equipment': self.supervisor_evaluation_lack_of_resources_equipment,
                        'supervisor_evaluation_lack_of_resources_human_resource': self.supervisor_evaluation_lack_of_resources_human_resource,
                        'supervisor_evaluation_lack_of_resources_information_technology': self.supervisor_evaluation_lack_of_resources_information_technology,
                        'supervisor_evaluation_lack_of_resources_other': self.supervisor_evaluation_lack_of_resources_other,
                        'supervisor_evaluation_factors_to_enhance_learning_more_time': self.supervisor_evaluation_factors_to_enhance_learning_more_time,
                        'supervisor_evaluation_factors_to_enhance_learning_others': self.supervisor_evaluation_factors_to_enhance_learning_others,
                        'supervisor_evaluation_extent_assisted_staff_subordinates': self.supervisor_evaluation_extent_assisted_staff_subordinates,
                        'self_evaluation_date': today.strftime('%Y-%m-%d'),
                        'state': 'training_supervisor_evaluated'
                        })
                else:
                    pass
        return True