# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TypeOfTraining(models.Model):
    _name = "type.of.training"
    _description = "type of training"
    name = fields.Char(string="Name", required=True)
    status = fields.Char(string="Status", required=True)

