from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from datetime import *
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char()
    age = fields.Integer(copy=False, tracking=True, compute='_compute_age', store=True)

    def _default_birthday_date(self):
        birthday = self.env['ir.config_parameter'].sudo().get_param('my_module.birthday')
        return birthday

    birthday = fields.Date(default=_default_birthday_date)

    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default='draft'
    )
    active = fields.Boolean(default=True)

    grade_teacher = fields.Many2one('teachers', string="Grade Teacher")
    grade = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3')], string="Grade"
    )

    img = fields.Binary()

    code = fields.Char(string="Number", required=True, copy=False,
                       default=lambda self: self.env['ir.sequence'].next_by_code('sequence.student'))

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    def update_existing_students(self):
        # Fetch the current student (assuming you're calling this method within a student record)
        current_student = self

        if current_student.code != _('Old'):
            # Set the value to "Old" and remove the old sequence
            current_student.write({'code': _('Old')})

    def update_all_students(self):
        all_students = self.search([])
        for student in all_students:
            if student.code != _('Old'):
                student.write({'code': _('Old')})

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age = 0

    @api.constrains('grade', 'grade_teacher')
    def _check_grade_before_save(self):
        for rec in self:
            if rec.grade != rec.grade_teacher.grade:
                raise ValidationError(_("Change Grade Teacher to Match the New Grade"))


class teachers(models.Model):
    _name = 'teachers'
    _description = 'This Model Represents the Teachers Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char()
    age = fields.Integer(copy=False, tracking=True, compute='_compute_age', store=True)
    birthday = fields.Date()
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default='draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )

    note = fields.Text(string="Note")
    active = fields.Boolean(default=True)

    grade = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3')], string="Grade"
    )

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age = 0

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'


