# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class TrainingPlan(models.Model):
    _name = "training.plan"
    _inherit = ["mail.thread"]
    _description = "training plan"
    # name = fields.Char(string="Ministry", required=True)
    name = fields.Many2one("res.company", string="Ministry")
    province = fields.Many2one("training.province", string="Province")
    # province = fields.Char(string="Province", required=True)
    institution = fields.Char(string="Institution", required=True)
    yearOfPlan = fields.Char(string="Year", required=True)
    supervisor_id = fields.Many2one("hr.employee", string="Supervisor")
    reference = fields.Char(
        string="Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    training_plan_line_ids = fields.One2many('training.plan.lines', 'training_plan_id', string="Training Plan Lines")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("hrdc", "HRDC"),
            ("ps", "PS"),
            ("psmd", "PSMD"),
            ("approved", "Approved"),
        ],
        default='draft',
        string="Status",
        required=True,
        tracking=True

    )
    hrdcComment = fields.Text(string="HRDC Comment", tracking=True)
    psComment = fields.Text(string="PS Comment", tracking=True)
    psmdComment = fields.Text(string="PSMD Comment", tracking=True)

    def action_save_training_plan_as_draft(self):
        self.write({'state': 'draft'})

    def action_submit_training_plan_to_hrdc(self):
        self.write({'state': 'hrdc'})

    def action_hrdc_approve_training_plan(self):
        self.write({'state': 'ps'})

    def action_hrdc_send_back_training_plan(self):
        self.write({'state': 'draft'})

    def action_ps_approve_training_plan(self):
        self.write({'state': 'psmd'})

    def action_ps_send_back_training_plan(self):
        self.write({'state': 'hrdc'})

    def action_psmd_approve_training_plan(self):
        self.write({'state': 'approved'})

        for line in self.training_plan_line_ids:
            employee = line.employee_id
            if employee.user_id and employee.user_id.email:
                # Sending email
                mail_values = {
                    'subject': 'Approved Training - ' + employee.name,
                    'body_html': """<p>You have been shortlisted to attend a training and your training program has been approved.</p><p> Click <a href='http://localhost:8069'>here</a> to log in and access the request.</p>""",
                    'email_to': employee.user_id.email,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()

    def action_psmd_send_back_training_plan(self):
        self.write({'state': 'ps'})

    @api.model
    def create(self, vals):
        current_year_month = datetime.now().strftime('%Y%m')
        sequence_code = self.env['ir.sequence'].next_by_code('training.plan') or _('Invalid')
        vals['reference'] = f"{current_year_month}-{sequence_code}"
        res = super(TrainingPlan, self).create(vals)
        return res


class TrainingPlanLines(models.Model):
    _name = "training.plan.lines"
    _description = "training plan lines"

    @api.constrains('self_evaluation_able_to_apply_knowledge', 'self_evaluation_hindering_factors_lack_of_resources')
    def _check_hindering_factors(self):
        for record in self:
            if record.self_evaluation_able_to_apply_knowledge == 'no':
                if not any([
                    record.self_evaluation_hindering_factors_lack_of_understanding,
                    record.self_evaluation_hindering_factors_supervisor_priorities_other,
                    record.self_evaluation_hindering_factors_constant_changes,
                    record.self_evaluation_hindering_factors_processes_not_flexible,
                    record.self_evaluation_hindering_factors_unclear_responsibilities,
                    record.self_evaluation_hindering_factors_not_enough_time,
                    record.self_evaluation_hindering_factors_not_relevant_to_current_job,
                    record.self_evaluation_hindering_factors_unclear_work_plans,
                    record.self_evaluation_hindering_factors_lack_of_resources,
                    record.self_evaluation_hindering_factors_other,
                ]):
                    raise ValidationError(
                        _("Please specify at least one hindering factor if you answered 'No' to applying the knowledge."))

            if not record.self_evaluation_hindering_factors_lack_of_resources:
                if any([
                    record.self_evaluation_lack_of_resources_finances,
                    record.self_evaluation_lack_of_resources_equipment,
                    record.self_evaluation_lack_of_resources_human_resource,
                    record.self_evaluation_lack_of_resources_information_technology,
                    record.self_evaluation_lack_of_resources_other,
                ]):
                    raise ValidationError(
                        _("Please specify 'Lack of resources' in Question 6 if you have filled any options in Question 7."))

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
        ('not_applied', 'Not Applied For Authority To Study'),
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
    is_current_user_employee = fields.Boolean(compute='_compute_is_current_user_employee', store=False)
    is_current_user_applicant = fields.Boolean(compute='_compute_should_show_apply', store=False)
    is_current_user_already_applicant = fields.Boolean(compute='_compute_should_show_applied', store=False)
    hod_comment = fields.Text(string='HOD Comment', tracking=True)
    bonding_date = fields.Date(string='Bonding Date')
    bonding_start_date = fields.Date(string='Bonding Start Date')
    bonding_end_date = fields.Date(string='Bonding End Date')
    rejection_comment = fields.Text(string='Rejection Comment')
    confirmation_status = fields.Text(string='Confirmation Status')
    ps_comment = fields.Text(string='PS Comment')
    employee_type = fields.Char(compute='_compute_employee_type', string='Employee Type', store=True)
    self_evaluation_date = fields.Date(string='Self Evaluation Date')
    supervisor_evaluation_date = fields.Date(string='Supervisor Evaluation Date')

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

    # Question 5
    self_evaluation_able_to_apply_knowledge = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Are you able to apply the Knowledge, Skills and Attitude acquired from the training to your job?",
        default='yes',
    )

    # Question 6 - Hindering Factors
    self_evaluation_hindering_factors_lack_of_understanding = fields.Boolean(
        string="Lack of understanding from your subordinates and/or colleagues",
        default=False,
    )
    self_evaluation_hindering_factors_supervisor_priorities_other = fields.Boolean(
        string="The Supervising Officer has other priorities",
        default=False,
    )
    self_evaluation_hindering_factors_constant_changes = fields.Boolean(
        string="Constant changes within the Ministry/Province/Institution",
        default=False,
    )
    self_evaluation_hindering_factors_processes_not_flexible = fields.Boolean(
        string="The systems, procedures and work processes are not flexible enough",
        default=False,
    )
    self_evaluation_hindering_factors_unclear_responsibilities = fields.Boolean(
        string="Levels of authority and responsibilities are not clear",
        default=False,
    )
    self_evaluation_hindering_factors_not_enough_time = fields.Boolean(
        string="Not enough time due to pressure of work",
        default=False,
    )
    self_evaluation_hindering_factors_not_relevant_to_current_job = fields.Boolean(
        string="Learning content of the course was not relevant to current job",
        default=False,
    )
    self_evaluation_hindering_factors_unclear_work_plans = fields.Boolean(
        string="Departmental/Unit Work Plans are not clear and specific",
        default=False,
    )
    self_evaluation_hindering_factors_lack_of_resources = fields.Boolean(
        string="Lack of resources",
        default=False,
    )
    self_evaluation_hindering_factors_other = fields.Text(
        string="Others, (Specify)",
        default=False,
    )

    # Question 7 - Lack of Resources
    self_evaluation_lack_of_resources_finances = fields.Boolean(
        string="Finances",
        default=False,
    )
    self_evaluation_lack_of_resources_equipment = fields.Boolean(
        string="Equipment",
        default=False,
    )
    self_evaluation_lack_of_resources_human_resource = fields.Boolean(
        string="Human Resource",
        default=False,
    )
    self_evaluation_lack_of_resources_information_technology = fields.Boolean(
        string="Information Technology",
        default=False,
    )
    self_evaluation_lack_of_resources_other = fields.Text(
        string="Others, (Specify)",
        default=False,
    )



    # Question 8 - Factors to enhance learning
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

    # Question 9 - Extent Assisted Staff
    self_evaluation_extent_assisted_staff_subordinates = fields.Selection(
        selection=[
            ("not_at_all", "Not at all"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("very_much", "Very much"),
        ],
        string="Your subordinates",
        tracking=True,
    )

    self_evaluation_extent_assisted_staff_supervisor = fields.Selection(
        selection=[
            ("not_at_all", "Not at all"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("very_much", "Very much"),
        ],
        string="Your Supervisor",
        tracking=True,
    )

    self_evaluation_extent_assisted_staff_colleagues = fields.Selection(
        selection=[
            ("not_at_all", "Not at all"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("very_much", "Very much"),
        ],
        string="Your colleagues",
        tracking=True,
    )
# # Question 9 - Extent Assisted Staff
#     self_evaluation_extent_assisted_staff_subordinates = fields.Selection(
#         selection=[
#             ("extent_assisted_staff_subordinates_1", "1"),
#             ("extent_assisted_staff_subordinates_2", "2"),
#             ("extent_assisted_staff_subordinates_3", "3"),
#             ("extent_assisted_staff_subordinates_4", "4"),
#             ("extent_assisted_staff_subordinates_5", "5"),
#         ],
#         string="Your subordinates", tracking=True,
#     )
#
#     self_evaluation_extent_assisted_staff_supervisor = fields.Selection(
#         selection=[
#             ("extent_assisted_staff_supervisor_1", "1"),
#             ("extent_assisted_staff_supervisor_2", "2"),
#             ("extent_assisted_staff_supervisor_3", "3"),
#             ("extent_assisted_staff_supervisor_4", "4"),
#             ("extent_assisted_staff_supervisor_5", "5"),
#         ],
#         string="Your Supervisor", tracking=True,
#     )
#
#     self_evaluation_extent_assisted_staff_colleagues = fields.Selection(
#         selection=[
#             ("extent_assisted_staff_colleagues_1", "1"),
#             ("extent_assisted_staff_colleagues_2", "2"),
#             ("extent_assisted_staff_colleagues_3", "3"),
#             ("extent_assisted_staff_colleagues_4", "4"),
#             ("extent_assisted_staff_colleagues_5", "5"),
#         ],
#         string="Your colleagues", tracking=True,
#     )

    self_evaluation_comments_other = fields.Text(string="Any other comments relating to the application of your training.")

    # self_evaluation_facility_rating_other = fields.Text(
    #     string="Please add any other comments that feel would improve the course.")

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
        default=False)

    supervisor_evaluation_hindering_factors_lack_of_understanding = fields.Boolean(
        string="Lack of understanding from his/her subordinates and/or colleagues",
        default=False)
    # supervisor_evaluation_hindering_factors_supervisor_priorities_other = fields.Boolean(string="You have other priorities",
    #                                                                default=False, required=True)
    supervisor_evaluation_hindering_factors_constant_changes = fields.Boolean(
        string="Constant changes within the Ministry/Province/Institution",
        default=False)
    supervisor_evaluation_hindering_factors_processes_not_flexible = fields.Boolean(
        string="The systems, procedures and work processes are not flexible enough",
        default=False)
    # supervisor_evaluation_hindering_factors_unclear_responsibilities = fields.Boolean(
    #     string="Levels of authority and responsibilities are not clear",
    #     default=False, required=True)
    supervisor_evaluation_hindering_factors_not_enough_time = fields.Boolean(
        string="Not enough time due to pressure of work",
        default=False)
    # supervisor_evaluation_hindering_factors_not_relevant_to_current_job = fields.Boolean(
    #     string="Learning content of the course was not relevant to current job",
    #     default=False, required=True)
    supervisor_evaluation_hindering_factors_unclear_work_plans = fields.Boolean(
        string="Departmental/Unit Work Plans are not clear and specific",
        default=False)
    supervisor_evaluation_hindering_factors_lack_of_resources = fields.Boolean(string="Lack of resources",
                                                                               default=False, required=True)
    supervisor_evaluation_hindering_factors_other = fields.Boolean(string="Others, (Specify)",
                                                                   default=False)

    supervisor_evaluation_lack_of_resources_finances = fields.Boolean(string="Finances", default=False, required=True)
    supervisor_evaluation_lack_of_resources_equipment = fields.Boolean(string="Equipment", default=False, required=True)
    supervisor_evaluation_lack_of_resources_human_resource = fields.Boolean(string="Human Resource", default=False,
                                                                            required=True)
    supervisor_evaluation_lack_of_resources_information_technology = fields.Boolean(string="Information Technology",
                                                                                    default=False)
    supervisor_evaluation_lack_of_resources_other = fields.Boolean(string="Others, (Specify)", default=False)

    supervisor_evaluation_factors_to_enhance_learning_more_training = fields.Boolean(string="More training",
                                                                                     default=False)
    # supervisor_evaluation_factors_to_enhance_learning_right_job_placement = fields.Boolean(string="Being placed in the right job",
    #                                                                  default=False, required=True)
    supervisor_evaluation_factors_to_enhance_learning_more_time = fields.Boolean(
        string="More time to practice the acquired knowledge and skills", default=False)
    # supervisor_evaluation_factors_to_enhance_learning_supervisor_Support = fields.Boolean(string="Support from my Supervising Officer",
    #                                                                 default=False, required=True)
    # supervisor_evaluation_factors_to_enhance_learning_modern_equipment = fields.Boolean(string="Modern Equipment", default=False,
    #                                                               required=True)
    supervisor_evaluation_factors_to_enhance_learning_others = fields.Boolean(string="Others, (specify)", default=False)

    supervisor_evaluation_extent_assisted_staff_subordinates = fields.Selection(
        selection=[
            ("extent_assisted_staff_subordinates_1", "1"),
            ("extent_assisted_staff_subordinates_2", "2"),
            ("extent_assisted_staff_subordinates_3", "3"),
            ("extent_assisted_staff_subordinates_4", "4"),
            ("extent_assisted_staff_subordinates_5", "5"),
        ],
        string="Your subordinates", tracking=True
    )

    supervisor_evaluation_extent_assisted_staff_supervisor = fields.Selection(
        selection=[
            ("extent_assisted_staff_supervisor_1", "1"),
            ("extent_assisted_staff_supervisor_2", "2"),
            ("extent_assisted_staff_supervisor_3", "3"),
            ("extent_assisted_staff_supervisor_4", "4"),
            ("extent_assisted_staff_supervisor_5", "5"),
        ],
        string="Your Supervisor", tracking=True
    )

    supervisor_evaluation_extent_assisted_staff_colleagues = fields.Selection(
        selection=[
            ("extent_assisted_staff_colleagues_1", "1"),
            ("extent_assisted_staff_colleagues_2", "2"),
            ("extent_assisted_staff_colleagues_3", "3"),
            ("extent_assisted_staff_colleagues_4", "4"),
            ("extent_assisted_staff_colleagues_5", "5"),
        ],
        string="Your colleagues", tracking=True
    )

    supervisor_evaluation_usefulness_other = fields.Char(string="Others, specify")

    supervisor_evaluation_facility_rating_other = fields.Text(
        string="Please add any other comments that feel would improve the course.")

    # Ensure the employee type is not 'student'
    @api.constrains('employee_type', 'state')
    def _check_employee_type(self):
        for record in self:
            if record.employee_type == 'student':
                raise ValidationError(_("Only confirmed Employees can proceed with the application."))

    supervisor_id = fields.Many2one('hr.employee', string="Supervisor", related='employee_id.parent_id')

    @api.depends('employee_id')
    def _compute_employee_type(self):
        for record in self:
            if record.employee_id:
                # Assuming the field name in 'hr.employee' is 'employee_type'
                # and it stores the selection value directly
                record.employee_type = record.employee_id.employee_type
            else:
                record.employee_type = None

    @api.depends('employee_id.user_id')
    def _compute_is_current_user_employee(self):
        for record in self:
            record.is_current_user_employee = record.employee_id.user_id.id == self.env.uid

    is_current_user_supervisor = fields.Boolean(compute='_compute_is_current_user_supervisor')
    is_current_user_hod = fields.Boolean(compute='_compute_is_current_user_hod')

    is_due_for_supervisor_evaluation = fields.Boolean(compute='_compute_is_due_for_supervisor_evaluation')
    is_current_user_self_evaluating = fields.Boolean(compute='_compute_self_evaluation')
    is_current_user_self_evaluated = fields.Boolean(compute='_compute_self_evaluated')
    is_current_user_owner = fields.Boolean(compute='_compute_own_application_show')

    @api.depends('employee_id', 'employee_id.parent_id.user_id', 'employee_id.parent_id.parent_id.user_id')
    def _compute_is_due_for_supervisor_evaluation(self):
        today = date.today()
        for record in self:
            if_is_current_user_supervisor = self.env.user == record.employee_id.parent_id.user_id
            if record.state == 'training_self_evaluation_evaluated' and record.self_evaluation_date:
                a = record.self_evaluation_date
                b = today
                months = (b.year - a.year) * 12 + b.month - a.month
                if months >= 3 and if_is_current_user_supervisor:
                    record.is_due_for_supervisor_evaluation = True
                else:
                    record.is_due_for_supervisor_evaluation = False
            else:
                record.is_due_for_supervisor_evaluation = False

    @api.depends('employee_id.user_id')
    def _compute_own_application_show(self):
        for record in self:
            record.is_current_user_owner = record.employee_id.user_id.id == self.env.uid

    @api.depends('state', 'employee_id.user_id')
    def _compute_self_evaluation(self):
        for record in self:
            record.is_current_user_self_evaluating = record.employee_id.user_id.id == self.env.uid and record.state == 'training_completed'

    @api.depends('state', 'employee_id.user_id')
    def _compute_self_evaluated(self):
        for record in self:
            record.is_current_user_self_evaluated = record.employee_id.user_id.id == self.env.uid and record.state == 'training_self_evaluation_evaluated'

    @api.depends('employee_id', 'employee_id.parent_id.user_id', 'employee_id.parent_id.parent_id.user_id')
    def _compute_is_current_user_supervisor(self):
        for record in self:
            record.is_current_user_supervisor = self.env.user == record.employee_id.parent_id.user_id

    @api.depends('employee_id.user_id')
    def _compute_should_show_apply(self):

        for record in self:
            record.is_current_user_applicant = record.employee_id.user_id.id == self.env.uid and record.state == 'not_applied'

    @api.depends('employee_id.user_id')
    def _compute_should_show_applied(self):
        for record in self:
            record.is_current_user_already_applicant = record.employee_id.user_id.id == self.env.uid and record.state != 'not_applied'

    def action_apply_for_authority_to_study(self):
        if self.state != 'not_applied':
            raise UserError(_("An application for this training has already been done."))
        self.ensure_one()  # Ensure this is called on a single record
        context = dict(self.env.context or {})
        context.update({
            'default_name': self.name,
            'default_employee_id': self.employee_id.id if self.employee_id else False,
            'default_priorityRanking': self.priorityRanking,
            'default_priorityArea': self.priorityArea,
            'default_level_of_training_proposed': self.level_of_training_proposed,
            'default_location_of_programme_proposed': self.location_of_programme_proposed.id,
            'default_proposed_date_of_programme': self.proposed_date_of_programme,
            'default_sponsor_id': self.sponsor_id.id,
            'default_justification_of_training': self.justification_of_training,
            'default_estimated_cost_per_year': self.estimated_cost_per_year,
            'default_training_plan_id': self.training_plan_id.id,
            'default_training_plan_state': self.training_plan_state,

        })
        return {
            'name': 'Applicaton for Authority to Study',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.training.plan.wizard.lines',
            'target': 'new',
            'context': context,
        }

    def action_self_evaluate_training(self):
        if self.state != 'training_completed':
            raise UserError(_("An evaluation of this training has already been done."))
        self.ensure_one()  # Ensure this is called on a single record
        context = dict(self.env.context or {})
        context.update({
            'default_name': self.name,
            'default_employee_id': self.employee_id.id if self.employee_id else False,
            'default_priorityRanking': self.priorityRanking,
            'default_priorityArea': self.priorityArea,
            'default_level_of_training_proposed': self.level_of_training_proposed,
            'default_location_of_programme_proposed': self.location_of_programme_proposed.id,
            'default_proposed_date_of_programme': self.proposed_date_of_programme,
            'default_sponsor_id': self.sponsor_id.id,
            'default_justification_of_training': self.justification_of_training,
            'default_estimated_cost_per_year': self.estimated_cost_per_year,
            'default_training_plan_id': self.training_plan_id.id,
            'default_training_plan_state': self.training_plan_state,

            # Add other fields you want to pass to the wizard
        })
        return {
            'name': 'Trainee Post Training Evaluation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.trainee.post.training.evaluation.wizard.lines',  # Update with your wizard model name
            'target': 'new',
            'context': context,
        }

    def action_supervisor_evaluate_training(self):
        if self.state != 'training_self_evaluation_evaluated':
            raise UserError(_("This evaluation is not available for your evaluation."))
        self.ensure_one()  # Ensure this is called on a single record
        context = dict(self.env.context or {})
        context.update({
            'default_name': self.name,
            'default_employee_id': self.employee_id.id if self.employee_id else False,
            'default_priorityRanking': self.priorityRanking,
            'default_priorityArea': self.priorityArea,
            'default_level_of_training_proposed': self.level_of_training_proposed,
            'default_location_of_programme_proposed': self.location_of_programme_proposed.id,
            'default_proposed_date_of_programme': self.proposed_date_of_programme,
            'default_sponsor_id': self.sponsor_id.id,
            'default_justification_of_training': self.justification_of_training,
            'default_estimated_cost_per_year': self.estimated_cost_per_year,
            'default_training_plan_id': self.training_plan_id.id,
            'default_training_plan_state': self.training_plan_state,

            # Add other fields you want to pass to the wizard
        })
        return {
            'name': 'Supervisor Post Training Evaluation',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.supervisor.post.training.evaluation.wizard.lines',
            # Update with your wizard model name
            'target': 'new',
            'context': context,
        }

    def action_save_application_as_draft(self):
        self.write({'state': 'not_applied'})

    def action_submit_application_to_supervisor(self):
        self.write({'state': 'supervisor'})

    def action_supervisor_approve_application(self):
        self.write({'state': 'hod'})

    def action_hrdc_send_back_training_plan(self):
        self.write({'state': 'draft'})

    def action_ps_approve_training_plan(self):
        self.write({'state': 'psmd'})

    def action_ps_send_back_training_plan(self):
        self.write({'state': 'hrdc'})

    def action_psmd_approve_training_plan(self):
        self.write({'state': 'approved'})

    def action_psmd_send_back_training_plan(self):
        self.write({'state': 'ps'})
