# -*- coding: utf-8 -*-
###############################################################################
#
#    Ministry of Health GRZ
#    Copyright (C) 2024-TODAY Ministry of Health GRZ(<https://www.moh.gov.zm>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api


class ScheduledTrainingCourse(models.Model):
    _name = "hrms.scheduled.training.course"
    _description = "Scheduled Training Course"

    name = fields.Char(string='Name')
    training_course_id = fields.Many2one(comodel_name='hrms.training.course', string='Training Course')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    participant_ids = fields.One2many(comodel_name='hr.employee', string='Participants')
    instructor_ids = fields.One2many(comodel_name='res.partner', string='Instructors')
    notes = fields.Text(string='Notes')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    district = fields.Char(string='District')
    province = fields.Char(string='Province')


