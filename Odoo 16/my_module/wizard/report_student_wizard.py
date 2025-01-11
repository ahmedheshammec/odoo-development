from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

class wizard_report_student(models.TransientModel):
    _name = 'wizard.report.student'
    show_all_grade = fields.Boolean(default=True)
    grade = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3')], string='Grade'
    )

    def print_report_pdf(self):
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'students',
            'form': data
        }
        return self.env.ref('my_module.students_details_report').report_action([], data=datas)

    def print_report_xlsx(self):
        data = {
            'form_data': self.read()[0],
        }
        return self.env.ref('my_module.students_details_xlsx').report_action(self, data=data)