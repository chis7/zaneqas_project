from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from odoo import _, SUPERUSER_ID


class EndOfCourseEvaluation(models.Model):
    _name = "training.course.evaluation"
    _description = "End of Course Evaluation"

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

    course_title = fields.Char(string="Course Title", required=True)
    date = fields.Date(string="Date", required=True)
    institution = fields.Char(string="Ministry/Province/Institution", required=True)
    duration = fields.Integer(string="Duration", required=True)

    pre_course_briefing = fields.Selection(
        selection=[
            ("pre_course_briefing_No", "No"),
            ("pre_course_briefing_Yes", "Yes"),
        ],
        string="Did you have a pre-course briefing?", tracking=True, required=True,
    )

    aware_of_objectives = fields.Selection(
        selection=[
            ("aware_of_objectives_No", "No"),
            ("aware_of_objectives_Yes", "Yes"),
        ],
        string="Were you aware of the objectives and aims of the course prior to attending it?", tracking=True,
        required=True,
    )

    prepared_and_ready = fields.Selection(
        selection=[
            ("prepared_and_ready_No", "No"),
            ("prepared_and_ready_Yes", "Yes"),
        ],
        string="Do you feel you were well prepared and ready to attend the course?", tracking=True, required=True,
    )
    relevant_to_job = fields.Selection(
        selection=[
            ("relevance_1", "1"),
            ("relevance_2", "2"),
            ("relevance_3", "3"),
            ("relevance_4", "4"),
            ("relevance_5", "5"),
        ],
        string="How relevant was the training to your job?", tracking=True, required=True,
    )
    confident_using_knowledge = fields.Selection(
        selection=[
            ("confidence_1", "1"),
            ("confidence_2", "2"),
            ("confidence_3", "3"),
            ("confidence_4", "4"),
            ("confidence_5", "5"),
        ],
        string="How confident do you feel about using the knowledge and skills covered in the course?", tracking=True, required=True,
    )
    extent_objectives_met = fields.Selection(
        selection=[
            ("extent_objectives_met_1", "1"),
            ("extent_objectives_met_2", "2"),
            ("extent_objectives_met_3", "3"),
            ("extent_objectives_met_4", "4"),
            ("extent_objectives_met_5", "5"),
        ],
        string="To what extent do you think the course objectives were met?", tracking=True, required=True,
    )
    usefulness_group_work = fields.Selection(
        selection=[
            ("usefulness_group_work_1", "1"),
            ("usefulness_group_work_2", "2"),
            ("usefulness_group_work_3", "3"),
            ("usefulness_group_work_4", "4"),
            ("usefulness_group_work_5", "5"),
        ],
        string="Group work", tracking=True, required=True,
    )

    usefulness_lectures = fields.Selection(
        selection=[
            ("usefulness_lectures_1", "1"),
            ("usefulness_lectures_2", "2"),
            ("usefulness_lectures_3", "3"),
            ("usefulness_lectures_4", "4"),
            ("usefulness_lectures_5", "5"),
        ],
        string="Lectures", tracking=True, required=True,
    )

    usefulness_overhead_transparencies = fields.Selection(
        selection=[
            ("usefulness_overhead_transparencies_1", "1"),
            ("usefulness_overhead_transparencies_2", "2"),
            ("usefulness_overhead_transparencies_3", "3"),
            ("usefulness_overhead_transparencies_4", "4"),
            ("usefulness_overhead_transparencies_5", "5"),
        ],
        string="Over Head Transparencies", tracking=True, required=True,
    )

    usefulness_stimulation_exercises = fields.Selection(
        selection=[
            ("usefulness_stimulation_exercises_1", "1"),
            ("usefulness_stimulation_exercises_2", "2"),
            ("usefulness_stimulation_exercises_3", "3"),
            ("usefulness_stimulation_exercises_4", "4"),
            ("usefulness_stimulation_exercises_5", "5"),
        ],
        string="Stimulation exercises", tracking=True, required=True,
    )

    usefulness_videos = fields.Selection(
        selection=[
            ("usefulness_videos_1", "1"),
            ("usefulness_videos_2", "2"),
            ("usefulness_videos_3", "3"),
            ("usefulness_videos_4", "4"),
            ("usefulness_videos_5", "5"),
        ],
        string="Videos or films", tracking=True, required=True,
    )

    usefulness_notes = fields.Selection(
        selection=[
            ("usefulness_notes_1", "1"),
            ("usefulness_notes_2", "2"),
            ("usefulness_notes_3", "3"),
            ("usefulness_notes_4", "4"),
            ("usefulness_notes_5", "5"),
        ],
        string="Notes and hand outs", tracking=True, required=True,
    )

    usefulness_discussions = fields.Selection(
        selection=[
            ("usefulness_discussions_1", "1"),
            ("usefulness_discussions_2", "2"),
            ("usefulness_discussions_3", "3"),
            ("usefulness_discussions_4", "4"),
            ("usefulness_discussions_5", "5"),
        ],
        string="Open discussions", tracking=True, required=True,
    )

    usefulness_other = fields.Char(string="Others, specify", required=False)

    enough_time_for_training = fields.Selection(
        selection=[
            ("enough_time_for_training_1", "1"),
            ("enough_time_for_training_2", "2"),
            ("enough_time_for_training_3", "3"),
            ("enough_time_for_training_4", "4"),
            ("enough_time_for_training_5", "5"),
        ],
        string="Enough time for training", tracking=True, required=True,
    )

    training_provider_rating_knowledge = fields.Selection(
        selection=[
            ("training_provider_rating_knowledge_1", "1"),
            ("training_provider_rating_knowledge_2", "2"),
            ("training_provider_rating_knowledge_3", "3"),
            ("training_provider_rating_knowledge_4", "4"),
            ("training_provider_rating_knowledge_5", "5"),
        ],
        string=" Knowledge of subject", tracking=True, required=True,
    )

    training_provider_rating_presentation = fields.Selection(
        selection=[
            ("training_provider_rating_presentation_1", "1"),
            ("training_provider_rating_presentation_2", "2"),
            ("training_provider_rating_presentation_3", "3"),
            ("training_provider_rating_presentation_4", "4"),
            ("training_provider_rating_presentation_5", "5"),
        ],
        string=" Presentation skills", tracking=True, required=True,
    )

    training_provider_rating_involving = fields.Selection(
        selection=[
            ("training_provider_rating_involving_1", "1"),
            ("training_provider_rating_involving_2", "2"),
            ("training_provider_rating_involving_3", "3"),
            ("training_provider_rating_involving_4", "4"),
            ("training_provider_rating_involving_5", "5"),
        ],
        string="Involving everyone", tracking=True, required=True,
    )

    training_provider_rating_pace = fields.Selection(
        selection=[
            ("training_provider_rating_pace_1", "1"),
            ("training_provider_rating_pace_2", "2"),
            ("training_provider_rating_pace_3", "3"),
            ("training_provider_rating_pace_4", "4"),
            ("training_provider_rating_pace_5", "5"),
        ],
        string="Correct pace", tracking=True, required=True,
    )

    training_provider_rating_availability = fields.Selection(
        selection=[
            ("training_provider_rating_availability_1", "1"),
            ("training_provider_rating_availability_2", "2"),
            ("training_provider_rating_availability_3", "3"),
            ("training_provider_rating_availability_4", "4"),
            ("training_provider_rating_availability_5", "5"),
        ],
        string="Availability", tracking=True, required=True,
    )

    training_provider_rating_visual_aids = fields.Selection(
        selection=[
            ("training_provider_rating_visual_aids_1", "1"),
            ("training_provider_rating_visual_aids_2", "2"),
            ("training_provider_rating_visual_aids_3", "3"),
            ("training_provider_rating_visual_aids_4", "4"),
            ("training_provider_rating_visual_aids_5", "5"),
        ],
        string="Use visual aids", tracking=True, required=True,
    )

    training_provider_rating_other = fields.Char(string="Others, specify", required=False)

    facility_rating_training_venue = fields.Selection(
        selection=[
            ("facility_rating_training_venue_1", "1"),
            ("facility_rating_training_venue_2", "2"),
            ("facility_rating_training_venue_3", "3"),
            ("facility_rating_training_venue_4", "4"),
            ("facility_rating_training_venue_5", "5"),
        ],
        string="Training Venue", tracking=True, required=True,
    )

    facility_rating_food = fields.Selection(
        selection=[
            ("facility_rating_food_1", "1"),
            ("facility_rating_food_2", "2"),
            ("facility_rating_food_3", "3"),
            ("facility_rating_food_4", "4"),
            ("facility_rating_food_5", "5"),
        ],
        string="Food", tracking=True, required=True,
    )

    facility_rating_accommodation = fields.Selection(
        selection=[
            ("facility_rating_accommodation_1", "1"),
            ("facility_rating_accommodation_2", "2"),
            ("facility_rating_accommodation_3", "3"),
            ("facility_rating_accommodation_4", "4"),
            ("facility_rating_accommodation_5", "5"),
        ],
        string="Accommodation", tracking=True, required=True,
    )

    facility_rating_service = fields.Selection(
        selection=[
            ("facility_rating_service_1", "1"),
            ("facility_rating_service_2", "2"),
            ("facility_rating_service_3", "3"),
            ("facility_rating_service_4", "4"),
            ("facility_rating_service_5", "5"),
        ],
        string="Service", tracking=True, required=True,
    )

    facility_rating_transport = fields.Selection(
        selection=[
            ("facility_rating_transport_1", "1"),
            ("facility_rating_transport_2", "2"),
            ("facility_rating_transport_3", "3"),
            ("facility_rating_transport_4", "4"),
            ("facility_rating_transport_5", "5"),
        ],
        string="Transport arrangement", tracking=True, required=True,
    )

    facility_rating_other = fields.Text(string="Please add any other comments that feel would improve the course.", required=False)

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
