from odoo import models, fields

class HRDepartment(models.Model):
    _inherit = 'hr.department'

    objectives = fields.One2many(
        comodel_name='hrms.departmental.objective',
        inverse_name='department_id',
        string='Objectives')
    work_plan_ids = fields.One2many(
        comodel_name='hrms.departmental.work.plan',
        inverse_name='department_id',
        string='Work Plans')

    # _sql_constraints = [
    #     ('unique_name',
    #      'unique(name)', 'Department should be unique!')]