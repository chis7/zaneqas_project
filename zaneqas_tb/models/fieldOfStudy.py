# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FieldOfStudy(models.Model):
    _name = "field.of.study"
    _description = "field of study"
    name = fields.Char(string="Name", required=True)
    status = fields.Char(string="Status", required=True)
