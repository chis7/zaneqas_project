# -*- coding: utf-8 -*-
import base64
import csv
from datetime import date
from io import StringIO

from odoo import api, fields, models
from odoo.exceptions import UserError


class ZaneqasTbXpertEqaExpectedResults(models.Model):
    _name = "zaneqas.tb.xpert.eqa.expected.result"
    _inherit = ["mail.thread"]
    _description = "zaneqas tb xpert eqa expected results"
    name = fields.Many2one("zaneqas.tb.xpert.eqa.config.rounds", required=True)
    due_date = fields.Date(string="Due Date", required=True)
    supervisor_comment = fields.Text(string="Supervisor Comment", tracking=True)

    # expected_result_lines_ids = fields.One2many(
    #     'zaneqas.tb.xpert.eqa.expected.result.lines',
    #     'zaneqas_tb_xpert_eqa_expected_result_id',
    #     string="Expected Result Lines"
    # )

    company_ids = fields.Many2many(
        'res.company',
        string='Facilities'
    )
    sample_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.expected.result.lines',
        'zaneqas_tb_xpert_eqa_expected_result_id',
        string="Samples"
    )

    zaneqas_tb_xpert_eqa_result_wizard_error_code_ids = fields.One2many(
        'zaneqas.tb.xpert.eqa.result.wizard.error.code.lines',
        'zaneqas_tb_xpert_eqa_result_wizard_error_code_id',
        string="Error Codes"
    )

    @api.onchange('name')
    def _onchange_name(self):
        self.sample_ids = [(5, 0, 0)]  # Clear existing values
        if self.name:
            samples = self.env['zaneqas.tb.xpert.eqa.rounds.sample.lines'].search(
                [('config_round_id', '=', self.name.id)])
            sample_markers = [(0, 0, {'sample_id': sample.sample_id}) for sample in samples]
            self.sample_ids = sample_markers

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("supervisor", "Supervisor"),
            ("approved", "Approved"),
            ("open", "Open"),
            ("extended", "Extended"),
            ("closed", "Closed"),
            ("resultsPublished", "Results Published"),
        ],
        default='draft',
        string="Status",
        required=True,
        tracking=True

    )
    lab_incharge_comment = fields.Char(string="Lab Incharge Comment", tracking=True)

    is_supervisor = fields.Boolean(compute='_compute_is_supervisor', store=False)
    is_LabIncharge = fields.Boolean(compute='_compute_is_labIncharge', store=False)
    current_state = fields.Char(compute='_compute_current_state')
    csv_file = fields.Binary(string="CSV File")
    csv_filename = fields.Char(string="CSV Filename")
    user_in_assigned_company_and_open = fields.Boolean(
        string="User in Assigned Company and Open",
        compute='_compute_user_in_assigned_company_and_open'
    )

    company_count = fields.Integer(string='Company Count', compute='_compute_company_count', store=True)

    # New field to check if the user belongs to a specific group
    user_has_group = fields.Boolean(
        string='User Has Group',
        compute='_compute_user_has_group'
    )

    site_id = fields.Many2one('res.partner', string='Name of Site')
    date_panel_received = fields.Date(string='Date Panel Received')
    date_of_last_gene_xpert_instrument_calibration_or_installation = fields.Date(
        string="Date of Last GeneXpert Instrument Calibration or Installation")
    xpert_assay_used = fields.Many2one('zaneqas.tb.xpert.eqa.config.assays')
    catridge_lot_number = fields.Char(string='Xpert MTB/RIF or Ultra Cartridge or Pouch Lot No:')
    expiry_date = fields.Date(string='Xpert MTB/RIF or Ultra Cartridge or Pouch Expiry Date')
    date_results_received_at_CDL = fields.Date(string='Date Results Received at CDL')
    add_infor_number_of_tests_conducted_in_last_full_month = fields.Integer(
        string="How many Xpert tests have been conducted in the last full month?", store=True)
    add_infor_number_of_errors_occurred = fields.Integer(
        string="How many errors occurred during testing in the past full month?", store=True)
    add_infor_was_monthly_maintenance_done_for_the_genexpert = fields.Selection(selection=[
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="Was monthly maintenance done for the GeneXpert?", store=True)
    add_infor_monthly_maintenance_done_by_date = fields.Date(string="Monthly maintenance done by Date",
                                                             store=True)
    add_infor_monthly_maintenance_done_by_technologist = fields.Char(string="Monthly maintenance done by technologist",
                                                                      store=True)
    add_infor_gene_xpert_serial_number = fields.Char(string="GeneXpert Serial Number", store=True)
    add_infor_date_gene_xpert_instrument_installed = fields.Date(string="Date GeneXpert Instrument Installed",
                                                                 store=True)
    add_infor_instrument_user = fields.Char(string="Instrument User (Tester)", store=True)
    declaration_testing_personnel = fields.Char(string="Testing Personnel", store=True)
    declaration_testing_personnel_date = fields.Date(string="Date", store=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    def save_wizard_data(self):
        # Implement the save logic here
        pass

    def validate_csv_file(self, csv_content):
        csv_reader = csv.reader(StringIO(csv_content))
        headers = next(csv_reader, None)
        if headers != ['Company Name']:
            raise UserError("Invalid CSV format. The header should be 'Company Name'.")

        for row in csv_reader:
            if len(row) != 1:
                raise UserError("Invalid CSV format. Each row should have exactly one column.")
            if not row[0].strip():
                raise UserError("Invalid CSV format. Company name cannot be empty.")

    def action_test_upload(self):
        if not self.csv_file:
            raise UserError("Please upload a CSV file first.")

        csv_content = base64.b64decode(self.csv_file).decode('utf-8')
        self.validate_csv_file(csv_content)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'CSV Validation',
                'message': 'The CSV file is valid.',
                'type': 'success',
                'sticky': False,
            }
        }

    @api.depends('company_ids')
    def _compute_company_count(self):
        for record in self:
            record.company_count = len(record.company_ids)

    def _compute_user_in_assigned_company_and_open(self):
        for record in self:
            user_company = self.env.user.company_id
            record.user_in_assigned_company_and_open = user_company in record.company_ids and record.state == 'open'

    def download_csv_template(self):
        csv_content = StringIO()
        csv_writer = csv.writer(csv_content)
        csv_writer.writerow(['Company Name'])  # Add more headers if needed

        # Fetch all companies and write to CSV
        companies = self.env['res.company'].search([])
        for company in companies:
            csv_writer.writerow([company.name])

        csv_data = base64.b64encode(csv_content.getvalue().encode('utf-8'))
        csv_content.close()

        attachment = self.env['ir.attachment'].create({
            'name': 'company_template.csv',
            'datas': csv_data,
            'type': 'binary',
            'res_model': self._name,
            'res_id': self.id,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def import_companies_from_csv(self):
        if not self.csv_file:
            raise UserError("Please upload a CSV file first.")

        csv_content = base64.b64decode(self.csv_file).decode('utf-8')
        csv_reader = csv.reader(StringIO(csv_content))
        next(csv_reader)  # Skip headers
        company_ids = []
        for row in csv_reader:
            company_name = row[0]
            company = self.env['res.company'].search([('name', '=', company_name)], limit=1)
            if company:
                company_ids.append(company.id)
            else:
                raise UserError(f"Company '{company_name}' not found.")
        self.company_ids = [(6, 0, company_ids)]

    @api.depends('state')
    def _compute_current_state(self):
        for record in self:
            record.current_state = record.state

    @api.depends('create_uid')
    def _compute_is_supervisor(self):
        for record in self:
            record.is_supervisor = self.env.user == record.create_uid.parent_id and record.state == 'supervisor'

    @api.depends('create_uid')
    def _compute_is_labIncharge(self):
        for record in self:
            record.is_LabIncharge = self.env.user == record.create_uid.parent_id.parent_id and record.state == 'lab_incharge'

    def action_save_eqa_result_as_draft(self):
        self.write({'state': 'draft'})

    def action_submit_eqa_result_to_supervisor(self):
        self.write({'state': 'supervisor'})

    def action_supervisor_approve_eqa_result(self):
        self.write({'state': 'lab_incharge'})

    def action_supervisor_send_back_eqa_result(self):
        self.write({'state': 'draft'})

    def action_LabIncharge_send_back_eqa_result(self):
        self.write({'state': 'lab_incharge'})

    def action_LabIncharge_approve_eqa_result(self):
        self.write({'state': 'approved'})

    def action_open_eqa_result(self):
        self.write({'state': 'open'})
        self.action_send_email_to_companies()

    def action_submit_results(self):
        # Implement the logic for submitting results
        pass

    def action_send_email_to_companies(self):
        for company in self.company_ids:
            if company.email:
                mail_values = {
                    'subject': 'Notification of TB Gene Xpert EQA',
                    'body_html': """<p>Dear {company_name},</p>
                                    <p>Please be informed that you have been selected to participate in the TB Gene Xpert EQA.</p>
                                    <p>Thank you.</p>""".format(company_name=company.name),
                    'email_to': company.email,
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()
