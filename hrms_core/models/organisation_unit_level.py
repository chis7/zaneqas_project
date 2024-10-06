from odoo import fields, models, api
from odoo.exceptions import ValidationError


class OrganisationUnitLevel(models.Model):
    _name = 'hrms.organisation.unit.level'
    _description = "Organisation Unit Level"
    _order = "id desc"

    uid = fields.Char(string='UID')
    name = fields.Char(string='Name', required=True)
    level = fields.Integer(string='Level', required=True)
    description = fields.Text(string='Description')
    organisation_unit_ids = fields.One2many(
        comodel_name='res.company',
        inverse_name='organisation_unit_level_id',
        string='Organisation Units')

    _sql_constraints = [
        ('unique_uid', 'UNIQUE(uid)', 'The UID must be unique.'),
        ('unique_name', 'UNIQUE(name)', 'The name must be unique.'),
        ('unique_level', 'UNIQUE(level)', 'The level must be unique.'),
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

    @api.constrains('level')
    def _check_unique_level(self):
        for record in self:
            if self.search_count([('level', '=', record.level)]) > 1:
                raise ValidationError('The level must be unique.')

