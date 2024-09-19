from odoo import fields, models, api
from odoo.exceptions import ValidationError


class OrganisationUnitGroup(models.Model):
    _name = 'hrms.organisation.unit.group'
    _description = "Organisation Unit Group"
    _order = "id desc"

    uid = fields.Char(string='UID', required=True)
    code = fields.Char(string='Code')
    short_name = fields.Char(string='Short Name')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    organisation_unit_group_set_id = fields.Many2one(
        comodel_name='hrms.organisation.unit.group.set',
        string='Organisation Unit Group Set')
    organisation_unit_ids = fields.Many2many(
        comodel_name='res.company',
        string='Organisation Units'
    )
    _sql_constraints = [
        ('unique_uid', 'UNIQUE(uid)', 'The UID must be unique.'),
        ('unique_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]

    @api.constrains('uid')
    def _check_unique_uid(self):
        for record in self:
            if self.search_count([('uid', '=', record.uid)]) > 1:
                raise ValidationError('The UID must be unique.')

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError('The name must be unique.')

