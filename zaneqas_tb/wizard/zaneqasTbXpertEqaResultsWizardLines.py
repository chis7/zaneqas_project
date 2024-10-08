# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaResultsWizardLines(models.TransientModel):
    _name = "zaneqas.tb.xpert.eqa.result.wizard.lines"
    _description = "Zaneqas TB Xpert EQA Results Wizard Lines"

    sample_id = fields.Char(string="Test Sample ID", required=True, store=True)
    date_tested = fields.Date(string="Date Tested", required=True, store=True)
    tb_detection_not_detected = fields.Boolean(string="Not Detected", store=True)
    tb_detection_trace = fields.Boolean(string="Trace", store=True)
    tb_detection_very_low = fields.Boolean(string="Very Low", store=True)
    tb_detection_low = fields.Boolean(string="Low", store=True)
    tb_detection_medium = fields.Boolean(string="Medium", store=True)
    tb_detection_high = fields.Boolean(string="High", store=True)
    rif_na = fields.Boolean(string="N/A", store=True)
    rif_not_detected = fields.Boolean(string="Not Detected", store=True)
    rif_detected = fields.Boolean(string="Detected", store=True)
    rif_indeterminate = fields.Boolean(string="Indeterminate", store=True)
    uninterpretable_invalid = fields.Boolean(string="Invalid", store=True)
    uninterpretable_no_result = fields.Boolean(string="No Result", store=True)
    uninterpretable_error = fields.Boolean(string="Error", store=True)
    uninterpretable_indeterminate = fields.Boolean(string="Indeterminate", store=True)
    uninterpretable_error_code = fields.Char(string="Error Code", store=True)
    ct_probe_d_ultra_spsc = fields.Float(string="Probe D/Ultra SPC", required=True, store=True)
    ct_probe_c_is1081_is6110 = fields.Float(string="Probe C/IS1081-IS6110", required=True, store=True)
    ct_probe_e_rpob2 = fields.Float(string="Probe E/rpoB2", required=True, store=True)
    ct_probe_b_rpoB1 = fields.Float(string="Probe B/rpoB1", required=True, store=True)
    ct_spc_rpoB3 = fields.Float(string="SPC/rpoB3", required=True, store=True)
    ct_probe_a_rpob4 = fields.Float(string="Probe A/rpoB4", required=True, store=True)
    ct_xpert_module_number = fields.Char(string="Xpert Module Number", required=True, store=True)
    zaneqas_tb_xpert_eqa_result_wizard_id = fields.Many2one('zaneqas.tb.xpert.eqa.result', string="zaneqas tb xpert eqa result", store=True)
    score = fields.Integer(string="Score", store=True)
