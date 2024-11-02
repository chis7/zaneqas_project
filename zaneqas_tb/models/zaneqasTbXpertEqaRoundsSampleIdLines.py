# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaRoundsSampleIdLines(models.Model):
    _name = "zaneqas.tb.xpert.eqa.rounds.sample.lines"
    _description = "Zaneqas TB Xpert EQA Rounds Sample ID Lines"

    # name = fields.Many2one('zaneqas.tb.xpert.eqa.config.rounds',string="Name", required=True)
    sample_id = fields.Char(string="Test Sample ID", required=True, store=True)

    config_round_id = fields.Many2one(
        'zaneqas.tb.xpert.eqa.config.rounds', string="Config Round ID", required=True
    )
    sample_ids = fields.Many2one(
        'zaneqas.tb.xpert.eqa.config.rounds', string="Config Round"
    )

    # expected_result_lines_ids = fields.One2many(
    #     'zaneqas.tb.xpert.eqa.expected.result.lines',
    #     'rounds_sample_line_id',
    #     string="Expected Result Lines"
    # )

