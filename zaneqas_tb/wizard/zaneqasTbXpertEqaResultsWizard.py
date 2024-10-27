# -*- coding: utf-8 -*-
from datetime import datetime, date

from odoo import api, fields, models, _, SUPERUSER_ID

from odoo.exceptions import UserError, ValidationError
import random


class ZaneqasTbXpertEqaResultsWizard(models.TransientModel):
    _name = "zaneqas.tb.xpert.eqa.result.wizard"
    _inherit = ["mail.thread"]
    _description = "zaneqas tb xpert eqa results"

    name = fields.Many2one('zaneqas.tb.xpert.eqa.expected.result', string="Cycle")
    site_id = fields.Many2one('res.partner', string='Name of Site')
    lab_code = fields.Char(string='Lab Code')
    site_contact_person = fields.Char(string='Site Contact Person')
    contact_email = fields.Char(string='Contact Email')
    date_panel_received = fields.Date(string='Date Panel Received', required=True)
    date_of_last_gene_xpert_instrument_calibration_or_installation = fields.Date(
        string="Date of Last GeneXpert Instrument Calibration or Installation", required=True)
    xpert_assay_used = fields.Many2one('zaneqas.tb.xpert.eqa.config.assays', required=True)
    catridge_lot_number = fields.Char(string='Xpert MTB/RIF or Ultra Cartridge or Pouch Lot No:', required=True)
    expiry_date = fields.Date(string='Xpert MTB/RIF or Ultra Cartridge or Pouch Expiry Date', required=True)
    comments = fields.Text(string='Comments')
    date_results_received_at_CDL = fields.Date(string='Date Results Received at CDL')
    add_infor_number_of_tests_conducted_in_last_full_month = fields.Integer(
        string="How many Xpert tests have been conducted in the last full month?", required=True, store=True)
    add_infor_number_of_errors_occurred = fields.Integer(
        string="How many errors occurred during testing in the past full month?", required=True, store=True)
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
    declaration_testing_personnel = fields.Char(string="Testing Personnel", store=True)
    declaration_testing_personnel_date = fields.Date(string="Date", store=True)
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)

    # zaneqas_tb_xpert_eqa_facility_result_id = fields.Many2one('zaneqas.tb.xpert.eqa.expected.result', string="facility eqa result", store=True)
    # zaneqas_tb_xpert_eqa_facility_result_id = fields.Many2one('zaneqas.tb.xpert.eqa.expected.result.lines', string="facility eqa result", store=True)

    zaneqas_tb_xpert_eqa_result_wizard_error_code_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.result.wizard.error.code.lines',
        'zaneqas_tb_xpert_eqa_result_wizard_error_code_id',
        string="ZANEQAS TB Xpert EQA Results Error Code Lines")
    zaneqas_tb_xpert_eqa_result_wizard_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.result.wizard.lines',
        'zaneqas_tb_xpert_eqa_result_wizard_id',
        string="ZANEQAS TB Xpert EQA Results Wizard Lines"
    )

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
    expected_result_lines_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.expected.result.lines', 'zaneqas_tb_xpert_eqa_expected_result_id',
        string='Expected Results'
    )

    supervisor_comment = fields.Text(string="Supervisor Comment", tracking=True)
    lab_incharge_comment = fields.Text(string="Lab Incharge Comment", tracking=True)
    results_status = fields.Char(string="Results Status", compute="_compute_results_status")
    company_name = fields.Char(string='Company Name', compute='_compute_company_name')
    state_of_cycle = fields.Selection(
        related='name.state',
        string="State of Cycle",
        readonly=True,
        store=True
    )
    sample_ids = fields.Many2many('zaneqas.tb.xpert.eqa.expected.result.line', string='Sample IDs')

    def default_get(self, fields):
        res = super(ZaneqasTbXpertEqaResultsWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            expected_result = self.env['zaneqas.tb.xpert.eqa.expected.result'].browse(active_id)
            if expected_result:
                eqa_round = expected_result.id
                expected_result_lines = self.env['zaneqas.tb.xpert.eqa.expected.result.lines'].search([
                    ('zaneqas_tb_xpert_eqa_expected_result_id', '=', eqa_round)
                ])
                res['expected_result_lines_ids'] = [(6, 0, expected_result_lines.ids)]
                res['name'] = expected_result.id

        else:
            raise ValueError("Invalid expected result record")
        return res

    def action_submit_results(self):
        active_id = self.env.context.get('active_id')
        expected_result_values = self.env['zaneqas.tb.xpert.eqa.expected.result.lines'].get_expected_result_values(
            active_id)

        # Use expected_result_values as needed
        # For example:
        self.write(expected_result_values)

    # def action_submit_results(self):
    #     active_id = self.env.context.get('active_id')
    #     form_data = {
    #         'name': self.name.id,
    #         'date_panel_received': self.date_panel_received,
    #         'date_of_last_gene_xpert_instrument_calibration_or_installation': self.date_of_last_gene_xpert_instrument_calibration_or_installation,
    #         'xpert_assay_used': self.xpert_assay_used.id,
    #         'expiry_date': self.expiry_date,
    #         'catridge_lot_number': self.catridge_lot_number,
    #         'add_infor_number_of_tests_conducted_in_last_full_month': self.add_infor_number_of_tests_conducted_in_last_full_month,
    #         'add_infor_number_of_errors_occurred': self.add_infor_number_of_errors_occurred,
    #         'add_infor_was_monthly_maintenance_done_for_the_genexpert': self.add_infor_was_monthly_maintenance_done_for_the_genexpert,
    #         'add_infor_monthly_maintenance_done_by_date': self.add_infor_monthly_maintenance_done_by_date,
    #         'add_infor_monthly_maintenance_done_by_technologist': self.add_infor_monthly_maintenance_done_by_technologist,
    #         'add_infor_gene_xpert_serial_number': self.add_infor_gene_xpert_serial_number,
    #         'add_infor_date_gene_xpert_instrument_installed': self.add_infor_date_gene_xpert_instrument_installed,
    #         'add_infor_instrument_user': self.add_infor_instrument_user,
    #     }
    #
    #     self.env['zaneqas.tb.xpert.eqa.result'].create(form_data)
    #
    #     for line in self.expected_result_lines_ids:
    #         form_data2 = {
    #             'sample_id': line.sample_id,
    #             'tb_detection_not_detected': line.tb_detection_not_detected,
    #             'tb_detection_trace': line.tb_detection_trace,
    #             'tb_detection_very_low': line.tb_detection_very_low,
    #             'tb_detection_low': line.tb_detection_low,
    #             'tb_detection_medium': line.tb_detection_medium,
    #             'tb_detection_high': line.tb_detection_high,
    #             'rif_na': line.rif_na,
    #             'rif_not_detected': line.rif_not_detected,
    #             'rif_detected': line.rif_detected,
    #             'rif_indeterminate': line.rif_indeterminate,
    #             'uninterpretable_invalid': line.uninterpretable_invalid,
    #             'uninterpretable_no_result': line.uninterpretable_no_result,
    #             'uninterpretable_error': line.uninterpretable_error,
    #             'uninterpretable_indeterminate': line.uninterpretable_indeterminate,
    #             'uninterpretable_error_code': line.uninterpretable_error_code,
    #             'ct_probe_d_ultra_spsc': line.ct_probe_d_ultra_spsc,
    #             'ct_probe_c_is1081_is6110': line.ct_probe_c_is1081_is6110,
    #             'ct_probe_e_rpob2': line.ct_probe_e_rpob2,
    #             'ct_probe_b_rpoB1': line.ct_probe_b_rpoB1,
    #             'ct_spc_rpoB3': line.ct_spc_rpoB3,
    #             'ct_probe_a_rpob4': line.ct_probe_a_rpob4,
    #             'ct_xpert_module_number': line.ct_xpert_module_number,
    #             'facility_result_date_tested': line.facility_result_date_tested,
    #             'facility_result_tb_detection_not_detected': line.facility_result_tb_detection_not_detected,
    #             'facility_result_tb_detection_trace': line.facility_result_tb_detection_trace,
    #             'facility_result_tb_detection_very_low': line.facility_result_tb_detection_very_low,
    #             'facility_result_tb_detection_low': line.facility_result_tb_detection_low,
    #             'facility_result_tb_detection_medium': line.facility_result_tb_detection_medium,
    #             'facility_result_tb_detection_high': line.facility_result_tb_detection_high,
    #             'facility_result_rif_na': line.facility_result_rif_na,
    #             'facility_result_rif_not_detected': line.facility_result_rif_not_detected,
    #             'facility_result_rif_detected': line.facility_result_rif_detected,
    #             'facility_result_rif_indeterminate': line.facility_result_rif_indeterminate,
    #             'facility_result_uninterpretable_invalid': line.facility_result_uninterpretable_invalid,
    #             'facility_result_uninterpretable_no_result': line.facility_result_uninterpretable_no_result,
    #             'facility_result_uninterpretable_error': line.facility_result_uninterpretable_error,
    #             'facility_result_uninterpretable_indeterminate': line.facility_result_uninterpretable_indeterminate,
    #             'facility_result_uninterpretable_error_code': line.facility_result_uninterpretable_error_code,
    #             'facility_result_ct_probe_d_ultra_spsc': line.facility_result_ct_probe_d_ultra_spsc,
    #             'facility_result_ct_probe_c_is1081_is6110': line.facility_result_ct_probe_c_is1081_is6110,
    #             'facility_result_ct_probe_e_rpob2': line.facility_result_ct_probe_e_rpob2,
    #             'facility_result_ct_probe_b_rpoB1': line.facility_result_ct_probe_b_rpoB1,
    #             'facility_result_ct_spc_rpoB3': line.facility_result_ct_spc_rpoB3,
    #             'facility_result_ct_probe_a_rpob4': line.facility_result_ct_probe_a_rpob4,
    #             'facility_result_ct_xpert_module_number': line.facility_result_ct_xpert_module_number,
    #             'zaneqas_tb_xpert_eqa_expected_result_id': line.zaneqas_tb_xpert_eqa_expected_result_id.id
    #             # Correctly assign the expected result ID
    #         }
    #         line.write(form_data2)
    #
    #     return {'type': 'ir.actions.act_window_close'}
