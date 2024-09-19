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


class TrainingCategory(models.Model):
    _name = "hrms.training.category"
    _description = "Training Category"

    name = fields.Char(string="Name")

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]


class TrainingModule(models.Model):
    _name = "hrms.training.module"
    _description = "Training Module"

    name = fields.Char(string="Name")
    training = fields.Many2one(comodel_name='hrms.training', string="Training")


class TrainingCourse(models.Model):
    _name = "hrms.training.course"
    _description = "Training Course"

    sequence = fields.Char(
        string='Reference',
        required=True, copy=False, readonly=True, index=True,
        default=lambda self: 'New')
    name = fields.Char(string='Name')
    topic = fields.Char(string='Topic')
    training_category_id = fields.Many2one(
        comodel_name='hrms.training.category',
        string='Training Category')
    training_institution_id = fields.Many2one(
        comodel_name='res.partner',
        string="Training Institution")
    status = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('closed', 'Closed'),
        ],
        string='Status'
    )
    certificate_template = fields.Html(string='Certificate Template')
    training_module_ids = fields.One2many(comodel_name='hrms.training.module', string='Training Module')
    competency_ids = fields.One2many(comodel_name='hrms.competency', string='Competencies')
    funder_ids = fields.One2many(comodel_name='hrms.funder', string='Funders')
    passing_score = fields.Float(string='Passing Score')
    cpd_points = fields.Float(string='CPD Points')
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active')

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Name should be unique!')]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hrms.competency.seq') or 'New'
            result = super(Competency, self).create(vals_list)
            return result