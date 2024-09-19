# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TrainingInstitutions(models.Model):
    _name = "training.training.institution"
    _description = "training institutions"
    name = fields.Char(string="Institution", required=True)
