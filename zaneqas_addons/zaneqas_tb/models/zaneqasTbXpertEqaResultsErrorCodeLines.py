# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaResultsErrorCodeLines(models.Model):
    _name = "zaneqas.tb.xpert.eqa.result.error.code.lines"
    _description = "Zaneqas TB Xpert EQA Results Error Code Lines"

    zaneqas_tb_xpert_eqa_result_error_code_id = fields.Many2one('zaneqas.tb.xpert.eqa.result',
                                                                string="zaneqas tb xpert eqa result error code",
                                                                )

    add_info_error_code = fields.Char(string="Error Codes", required=True, store=True)
