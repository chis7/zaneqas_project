from odoo import models, api

class ReportZaneqasTbXpertEqaResults(models.AbstractModel):
    _name = 'report.zaneqas.tb.report.zaneqas.tb.xpert.eqa.results'
    _description = 'GeneXpert EQA Results Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['zaneqas.tb.xpert.eqa.result'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'zaneqas.tb.xpert.eqa.result',
            'docs': docs,
        }