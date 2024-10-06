# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Sponsor(models.Model):
    _name = "training.sponsor"
    _description = "sponsors"
    name = fields.Char(string="Sponsor", required=True)
