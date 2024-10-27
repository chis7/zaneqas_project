# # File: zaneqas_addons/zaneqas_tb/report/gene_xpert_eqa_results.py
# from odoo import models, api
#
# class ReportGeneXpertEqaResults(models.AbstractModel):
#     _name = 'report.zaneqas.tb.report.gene.xpert.eqa.results'
#     _description = 'Gene Xpert EQA Results Report'
#
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['zaneqas.tb.xpert.eqa.expected.result'].browse(docids)
#         return {
#             'doc_ids': docids,
#             'doc_model': 'zaneqas.tb.xpert.eqa.expected.result',
#             'docs': docs,
#         }