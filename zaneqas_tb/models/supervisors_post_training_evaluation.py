from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from odoo import _, SUPERUSER_ID


class SupervisorPostTrainingEvaluation(models.Model):
    _name = "training.supervisor.post.evaluation"
    _description = "Supervisor Post training Evaluation"

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("supervisor_approved", "Supervisor Approved"),
            ("hod_approved", "HOD Approved"),
            ("approved", "Approved"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ], string="Status", default="draft")

    name = fields.Char(string="Name of former trainee:", required=True)
    institution = fields.Char(string="Ministry/Province/Institution", required=True)
    name_of_course = fields.Char(string="Name of course attended", required=True)
    date_attended = fields.Date(string='Date attended?', default=False, required=True)
    course_duration = fields.Char(string='Course Duration?', default=False, required=True)
    department = fields.Date(string="Date", required=True)
    gender = fields.Selection(
        selection=[
            ("gender_male", "male"),
            ("gender_female", "female"),
        ],
        string="Relevance of training to job", tracking=True, required=True,
    )
    age = fields.Selection(
        selection=[
            ("age_25_and_below", "25 or below"),
            ("age_26_30", "26_30"),
            ("age_31_35", "31_35"),
            ("age_36_40", "36_40"),
            ("age_41_45 ", "41_45"),
            ("age_41_45 ", "41_45"),
            ("age_41_45 ", "41_45"),
        ],
        string="Age", tracking=True, required=True,
    )
    main_course_objective = fields.Char(string='Main Course Objective', default=False, required=True)
    level_of_training = fields.Char(string='Level of Training', default=False, required=True)
    training_institution = fields.Char(string='Training Institution', default=False, required=True)
    Sponsor = fields.Char(string='Sponsor', default=False, required=True)

    extent_objectives_achieved_before = fields.Selection(
        selection=[
            ("extent_objectives_achieved_before_1", "1"),
            ("extent_objectives_achieved_before_2", "2"),
            ("extent_objectives_achieved_before_3", "3"),
            ("extent_objectives_achieved_before_4", "4"),
            ("extent_objectives_achieved_before_5", "5"),
        ],
        string="To what extent has the trainee been able to achieve the objectives/targets shown in the Departmental/Unit Work Plans before the training?",
        tracking=True, required=True,
    )

    extent_objectives_achieved_after = fields.Selection(
        selection=[
            ("extent_objectives_achieved_after_1", "1"),
            ("extent_objectives_achieved_after_2", "2"),
            ("extent_objectives_achieved_after_3", "3"),
            ("extent_objectives_achieved_after_4", "4"),
            ("extent_objectives_achieved_after_5", "5"),
        ],
        string="To what extent was the trainee able to achieve the objectives and targets stated in your Departmental/Unit Work plans after the training?",
        tracking=True, required=True,
    )
    extent_training_helped = fields.Selection(
        selection=[
            ("extent_training_helped_1", "1"),
            ("extent_training_helped_2", "2"),
            ("extent_training_helped_3", "3"),
            ("extent_training_helped_4", "4"),
            ("extent_training_helped_5", "5"),
        ],
        string="To what extent has the training helped you in achieving objectives and targets as stated in your Departmental/Unit Work Plans?",
        tracking=True, required=True,
    )
    performance_rating_before = fields.Selection(
        selection=[
            ("performance_rating_before_1", "1"),
            ("performance_rating_before_2", "2"),
            ("performance_rating_before_3", "3"),
            ("performance_rating_before_4", "4"),
            ("performance_rating_before_5", "5"),
        ],
        string="To what extent do you think this training has impacted on the trainee’s job performance?", tracking=True, required=True,
    )

    performance_rating_current = fields.Selection(
        selection=[
            ("performance_rating_current_1", "1"),
            ("performance_rating_current_2", "2"),
            ("performance_rating_current_3", "3"),
            ("performance_rating_current_4", "4"),
            ("performance_rating_current_5", "5"),
        ],
        string="How do you rate your job performance now?", tracking=True, required=True,
    )

    able_to_apply_knowledge = fields.Boolean(
        string="Has the trainee been able to apply knowledge, skills and attitudes acquired from the course to his/her job?",
        default=False,
        required=True)

    hindering_factors_lack_of_understanding = fields.Boolean(
        string="Lack of understanding from his/her subordinates and/or colleagues",
        default=False, required=True)
    hindering_factors_supervisor_priorities_other = fields.Boolean(string="You have other priorities",
                                                                   default=False, required=True)
    hindering_factors_constant_changes = fields.Boolean(
        string="Constant changes within the Ministry/Province/Institution",
        default=False, required=True)
    hindering_factors_processes_not_flexible = fields.Boolean(
        string="The systems, procedures and work processes are not flexible enough",
        default=False, required=True)
    hindering_factors_unclear_responsibilities = fields.Boolean(
        string="Levels of authority and responsibilities are not clear",
        default=False, required=True)
    hindering_factors_not_enough_time = fields.Boolean(string="Not enough time due to pressure of work",
                                                       default=False, required=True)
    hindering_factors_not_relevant_to_current_job = fields.Boolean(
        string="Learning content of the course was not relevant to current job",
        default=False, required=True)
    hindering_factors_unclear_work_plans = fields.Boolean(
        string="Departmental/Unit Work Plans are not clear and specific",
        default=False, required=True)
    hindering_factors_lack_of_resources = fields.Boolean(string="Lack of resources", default=False, required=True)
    hindering_factors_other = fields.Boolean(string="Others, (Specify)",
                                             default=False, required=True)

    lack_of_resources_finances = fields.Boolean(string="Finances", default=False, required=True)
    lack_of_resources_equipment = fields.Boolean(string="Equipment", default=False, required=True)
    lack_of_resources_human_resource = fields.Boolean(string="Human Resource", default=False, required=True)
    lack_of_resources_information_technology = fields.Boolean(string="Information Technology", default=False,
                                                              required=True)
    lack_of_resources_other = fields.Boolean(string="Others, (Specify)", default=False, required=True)

    factors_to_enhance_learning_more_training = fields.Boolean(string="More training", default=False, required=True)
    factors_to_enhance_learning_right_job_placement = fields.Boolean(string="Being placed in the right job",
                                                                     default=False, required=True)
    factors_to_enhance_learning_more_time = fields.Boolean(
        string="More time to practice the acquired knowledge and skills", default=False, required=True)
    factors_to_enhance_learning_supervisor_Support = fields.Boolean(string="Support from my Supervising Officer",
                                                                    default=False, required=True)
    factors_to_enhance_learning_modern_equipment = fields.Boolean(string="Modern Equipment", default=False,
                                                                  required=True)
    factors_to_enhance_learning_others = fields.Boolean(string="Others, (specify)", default=False, required=True)

    extent_assisted_staff_subordinates = fields.Selection(
        selection=[
            ("extent_assisted_staff_subordinates_1", "1"),
            ("extent_assisted_staff_subordinates_2", "2"),
            ("extent_assisted_staff_subordinates_3", "3"),
            ("extent_assisted_staff_subordinates_4", "4"),
            ("extent_assisted_staff_subordinates_5", "5"),
        ],
        string="Your subordinates", tracking=True, required=True,
    )

    extent_assisted_staff_supervisor = fields.Selection(
        selection=[
            ("extent_assisted_staff_supervisor_1", "1"),
            ("extent_assisted_staff_supervisor_2", "2"),
            ("extent_assisted_staff_supervisor_3", "3"),
            ("extent_assisted_staff_supervisor_4", "4"),
            ("extent_assisted_staff_supervisor_5", "5"),
        ],
        string="Your Supervisor", tracking=True, required=True,
    )

    extent_assisted_staff_colleagues = fields.Selection(
        selection=[
            ("extent_assisted_staff_colleagues_1", "1"),
            ("extent_assisted_staff_colleagues_2", "2"),
            ("extent_assisted_staff_colleagues_3", "3"),
            ("extent_assisted_staff_colleagues_4", "4"),
            ("extent_assisted_staff_colleagues_5", "5"),
        ],
        string="Your colleagues", tracking=True, required=True,
    )

    usefulness_other = fields.Char(string="Others, specify", required=False)

    facility_rating_other = fields.Text(string="Please add any other comments that feel would improve the course.",
                                        required=False)

    def action_confirm(self):
        return self.write({'state': 'confirm'})

    def action_done(self):
        return self.write({'state': 'done'})

    def action_draft(self):
        return self.write({'state': 'draft'})

    def action_cancel(self):
        return self.write({'state': 'cancel'})

    def action_supervisor_approve(self):
        if self.state == 'confirm' and (self.env.uid == self.supervisor_id.id or self.env.uid == SUPERUSER_ID):
            return self.write({'state': 'supervisor_approved'})
        else:
            raise UserError(_('Only the Supervisor can approve at this stage.'))

    def action_hod_approve(self):
        if self.state == 'supervisor_approved' and (self.env.uid == self.hod_id.id or self.env.uid == SUPERUSER_ID):
            return self.write({'state': 'hod_approved'})
        else:
            raise UserError(_('Only the HOD can approve at this stage.'))

    def action_ps_approve(self):
        if self.state == 'hod_approved' and (self.env.uid == self.ps_id.id or self.env.uid == SUPERUSER_ID):
            return self.write({'state': 'approved'})
        else:
            raise UserError(_('Only the PS can approve at this stage.'))