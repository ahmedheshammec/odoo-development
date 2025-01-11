from odoo import api, fields, models
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ReportStudentDetails(models.AbstractModel):
    _name = 'report.my_module.report_students_details'
    _description = 'Student Details'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data['form'].get('grade', False):
            students = self.env['students'].search([('grade', '=', data['form'].get('grade', False))])
            return {
                'students': students,
                'data': data['form'],
            }
        else:
            students = self.env['students'].search([])
            return {
                'students': students,
                'data': data['form'],
            }


class PartnerXlsx(models.AbstractModel):
    _name = 'report.my_module.students_details_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            if data['form_data'].get('grade', False):
                report_name = "Grade:" + str(data['form_data'].get('grade', False))
            else:
                report_name = "All Grade"

            if data['form_data'].get('grade', False):
                students = self.env['students'].search([('grade', '=', data['form_data'].get('grade', False))])
            else:
                students = self.env['students'].search([])

            sheet = workbook.add_worksheet(report_name)
            bold = workbook.add_format({'bold': True})
            date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
            align_center = workbook.add_format({'align': 'center'})
            align_center_b = workbook.add_format({'align': 'center', 'bold': True})
            row = 5
            col = 5
            sheet.write(row, col, 'Grade', bold)
            col += 1
            sheet.write(row, col, report_name)
            row += 1
            col -= 1
            col += 1
            if students:
                row += 2
                col = 1
                sheet.merge_range(row, col, row, col + 5, 'students', align_center)
                row += 1
                col = 1
                sheet.write(row, col, 'Name', bold)
                col += 1
                sheet.write(row, col, 'Age', bold)
                col += 1
                sheet.write(row, col, 'Grade', bold)
                row += 1
                col = 1
                for record in students:
                    sheet.write(row, col, record.name)
                    col += 1
                    sheet.write(row, col, record.age)
                    col += 1
                    sheet.write(row, col, record.grade)
                    col = 1
                    row += 1
        workbook.close()
