# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FieldOfStudy(models.Model):
    _name = "training.province"
    _description = "provinces"
    name = fields.Char(string="Province", required=True)
