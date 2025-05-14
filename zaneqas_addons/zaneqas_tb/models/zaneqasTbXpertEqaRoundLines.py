# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaRoundLines(models.Model):
    _name = "zaneqas.tb.xpert.eqa.config.rounds.lines"
    _description = "Zaneqas TB Xpert EQA Rounds Lines"

    zaneqas_tb_xpert_eqa_round_id = fields.Many2one('zaneqas.tb.xpert.eqa.config.rounds',
                                                                string="zaneqas tb xpert eqa rounds",
                                                                store=True)

    sample_id = fields.Char(string="Error Codes", required=True, store=True)