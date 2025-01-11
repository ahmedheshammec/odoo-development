from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date


class level(models.Model):
    _name = 'level'
    _description = 'This Class Represents the Students Level'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(string='Level')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    students_ids = fields.Many2many('students', string='Students')
    material_lines = fields.One2many('material', 'level_id', string='Materials')

    def action_view_material(self):
        material_lines = self.mapped('material_lines')
        domain = [('id', 'in', material_lines.ids)]
        context = {'default_level_id': self.id, }
        return {
            'name': _('Materials Lines'),
            'res_model': 'material',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': context,
            'type': 'ir.actions.act_window',
        }

class material(models.Model):
    _name = 'material'
    _description = 'This Class Represents the Materials'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(string='Material Name')
    grade_teacher = fields.Many2one('teachers')
    level_id = fields.Many2one('level')
    active = fields.Boolean(default=True)