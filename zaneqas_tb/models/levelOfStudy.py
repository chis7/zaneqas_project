# -*- coding: utf-8 -*-
from odoo import api, fields, models


class LevelOfStudy(models.Model):
    _name = "level.of.study"
    _description = "level of study"
    name = fields.Char(string="Name", required=True)
    status = fields.Char(string="Status", required=True)
