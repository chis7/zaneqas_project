# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaResults(models.Model):
    _name = "zaneqas.tb.xpert.eqa.result"
    _inherit = ["mail.thread"]
    _description = "zaneqas tb xpert eqa results"

    name = fields.Many2one('zaneqas.tb.xpert.eqa.expected.result', string="Cycle")
    due_date = fields.Date(related='name.due_date', string="Closing Date", store=True)
    # name = fields.Many2one('zaneqas.tb.xpert.eqa.config.rounds', string="PT Cycle #", required=True)
    site_id = fields.Many2one('res.partner', string='Name of Site')
    lab_code = fields.Char(string='Lab Code')
    site_contact_person = fields.Char(string='Site Contact Person')
    contact_email = fields.Char(string='Contact Email')
    date_panel_received = fields.Date(string='Date Panel Received', required=True)
    date_panel_reported = fields.Date(string='Date Results Reported', required=True)
    date_of_last_gene_xpert_instrument_calibration_or_installation = fields.Date(
        string="Date of Last GeneXpert Instrument Calibration or Installation", required=True)
    xpert_assay_used = fields.Char(string='Xpert Assay Used', required=True)
    catridge_lot_number = fields.Char(string='Xpert MTB/RIF or Ultra Cartridge or Pouch Lot No:', required=True)
    expiry_date = fields.Date(string='Xpert MTB/RIF or Ultra Cartridge or Pouch Expiry Date', required=True)
    comments = fields.Text(string='Comments')
    date_results_received_at_CDL = fields.Date(string='Date Results Received at CDL')
    add_infor_number_of_tests_conducted_in_last_full_month = fields.Integer(
        string="How many Xpert tests have been conducted in the last full month?", required=True, store=True)
    add_infor_number_of_errors_occurred = fields.Integer(
        string="How many errors occurred during testing in the past full month?", required=True, store=True)
    # add_info_error_codes = fields.Char(string="What are the Error Codes?", required=True, store=True)
    add_infor_was_monthly_maintenance_done_for_the_genexpert = fields.Selection(selection=[
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Was monthly maintenance done for the GeneXpert?", required=True, store=True)
    add_infor_monthly_maintenance_done_by_date = fields.Date(string="Monthly maintenance done by Date", required=True,
                                                             store=True)
    add_infor_monthly_maintenance_done_by_technologist = fields.Char(string="Monthly maintenance done by technologist",
                                                                     required=True, store=True)
    add_infor_gene_xpert_serial_number = fields.Char(string="GeneXpert Serial Number", required=True, store=True)
    add_infor_date_gene_xpert_instrument_installed = fields.Date(string="Date GeneXpert Instrument Installed",
                                                                 required=True, store=True)
    add_infor_instrument_user = fields.Char(string="Instrument User (Tester)", required=True, store=True)
    add_infor_supervisor_review_panel_results = fields.Selection(selection=[('yes', 'Yes'),
                                                                            ('no', 'No')],
                                                                 string="Did Supervisor Review Panel Results?",
                                                                 required=True, store=True)
    declaration_laboratory_in_charge = fields.Char(string="Laboratory In-Charge", required=True, store=True)
    declaration_laboratory_in_charge_date = fields.Date(string="Date", required=True, store=True)
    declaration_testing_personnel = fields.Char(string="Testing Personnel", store=True)
    declaration_testing_personnel_date = fields.Date(string="Date", store=True)

    zaneqas_tb_xpert_eqa_result_error_code_ids = fields.One2many('zaneqas.tb.xpert.eqa.result.error.code.lines',
                                                                 'zaneqas_tb_xpert_eqa_result_error_code_id',
                                                                 string="ZANEQAS TB Xpert EQA Results Error Code Lines")
    zaneqas_tb_xpert_eqa_result_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.result.lines',
        'zaneqas_tb_xpert_eqa_result_id',
        string="ZANEQAS TB Xpert EQA Results Lines"
    )

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.zaneqas_tb_xpert_eqa_result_ids = [(5, 0, 0)]  # Clear existing values
            expected_results = self.env['zaneqas.tb.xpert.eqa.expected.result'].browse(self.name.id)
            result_lines = [(0, 0, {'sample_id': line.sample_id}) for line in
                            expected_results.zaneqas_tb_xpert_eqa_expected_result_ids]
            self.zaneqas_tb_xpert_eqa_result_ids = result_lines

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("supervisor", "Supervisor"),
            ("lab_incharge", "Lab Incharge"),
            ("approved", "Approved"),
        ],
        default='draft',
        string="Status",
        required=True,
        tracking=True
    )
    supervisor_comment = fields.Text(string="Supervisor Comment", tracking=True)
    lab_incharge_comment = fields.Text(string="Lab Incharge Comment", tracking=True)
    results_status = fields.Char(string="Results Status", compute="_compute_results_status")
    company_name = fields.Integer(string="Company Name", store=True)

    tb_detection_not_detected = fields.Boolean(
        related='zaneqas_tb_xpert_eqa_result_ids.tb_detection_not_detected',
        string="MTB Detection - Not Detected",
        store=True
    )
    expected_result_lines_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.expected.result.lines',
        'zaneqas_tb_xpert_eqa_expected_result_id',
        string="Expected Results"
    )

    @api.depends('create_uid')
    def _compute_company_name(self):
        for record in self:
            record.company_name = record.create_uid.company_id.name if record.create_uid.company_id else ''

    @api.depends('date_results_received_at_CDL')
    def _compute_results_status(self):
        for record in self:
            record.results_status = "Not Received" if not record.date_results_received_at_CDL else "Received"

    def action_save_eqa_result_as_draft(self):

        company_name = self.env.user.company_id.id
        self.write({'state': 'draft',
                    'date_results_received_at_CDL': fields.Date.today(),
                    'company_name': company_name
                    })
        for actual_result in self.zaneqas_tb_xpert_eqa_result_ids:
            expected_result = self.env['zaneqas.tb.xpert.eqa.expected.result.lines'].search([
                ('sample_id', '=', actual_result.sample_id),
                ('zaneqas_tb_xpert_eqa_expected_result_id', '=', self.name.id)
            ], limit=1)
            if not expected_result:
                raise ValidationError(f"No expected result found for sample {actual_result.sample_id}")
            score = 0
            if (expected_result.tb_detection_not_detected == actual_result.tb_detection_not_detected and
                    expected_result.tb_detection_trace == actual_result.tb_detection_trace and
                    expected_result.tb_detection_very_low == actual_result.tb_detection_very_low and
                    expected_result.tb_detection_low == actual_result.tb_detection_low and
                    expected_result.tb_detection_medium == actual_result.tb_detection_medium and
                    expected_result.tb_detection_high == actual_result.tb_detection_high and
                    expected_result.rif_na == actual_result.rif_na and
                    expected_result.rif_not_detected == actual_result.rif_not_detected and
                    expected_result.rif_detected == actual_result.rif_detected
            ):
                score += 20
            if (expected_result.tb_detection_not_detected == actual_result.tb_detection_not_detected and
                        expected_result.tb_detection_trace == actual_result.tb_detection_trace and
                        expected_result.tb_detection_very_low == actual_result.tb_detection_very_low and
                        expected_result.tb_detection_low == actual_result.tb_detection_low and
                        expected_result.tb_detection_medium == actual_result.tb_detection_medium and
                        expected_result.tb_detection_high == actual_result.tb_detection_high
                ) and (actual_result.rif_indeterminate == True):
                    score += 10
            if (actual_result.uninterpretable_invalid or actual_result.uninterpretable_no_result or
                    actual_result.uninterpretable_error or actual_result.uninterpretable_indeterminate):
                score += 5
            if (actual_result.tb_detection_not_detected == False and
                    actual_result.tb_detection_trace == False and
                    actual_result.tb_detection_very_low == False and
                    actual_result.tb_detection_low == False and
                    actual_result.tb_detection_medium == False and
                    actual_result.tb_detection_high == False or
                    actual_result.rif_na == False and
                    actual_result.rif_not_detected == False and
                    actual_result.rif_detected == False):
                score = 0

            actual_result.write({'score': score})

    def action_submit_eqa_result_to_supervisor(self):
        self.write({'state': 'supervisor'})

    def action_supervisor_approve_eqa_result(self):
        self.write({'state': 'lab_incharge'})

    def action_supervisor_send_back_eqa_result(self):
        self.write({'state': 'draft'})

    def action_LabIncharge_send_back_eqa_result(self):
        self.write({'state': 'lab_incharge'})

    def action_LabIncharge_approve_eqa_result(self):
        self.write({'state': 'approved',
                    'date_results_received_at_CDL': fields.Date.today()})
