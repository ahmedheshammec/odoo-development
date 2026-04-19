from odoo import models, api, _, fields
from odoo.exceptions import UserError
import logging
import base64
import os
from weasyprint import HTML
import babel.dates
from num2words import num2words

_logger = logging.getLogger(__name__)


class Collections(models.Model):
    _inherit = 'collections.collections'
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id.id
    )

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    def _get_company_stamp_base64(self):
        self.ensure_one()
        company_stamp = self.res_association_id.x_studio_many2one_field_5j9_1j3lg5b21.company_stamp
        if company_stamp:
            return f"data:image/png;base64,{company_stamp.decode('utf-8') if isinstance(company_stamp, bytes) else company_stamp}"
        return None

    def _get_font_path(self, font_file):
        """Get absolute file path for font file"""
        try:
            module_path = os.path.dirname(os.path.dirname(__file__))
            font_path = os.path.join(module_path, 'static', 'fonts', font_file)
            if os.path.exists(font_path):
                return f"file://{font_path}"
        except Exception as e:
            _logger.error(f"Error getting font path: {e}")
        return None

    def _get_signature_base64(self):
        """Get signature image as base64"""
        try:
            module_path = os.path.dirname(os.path.dirname(__file__))
            signature_path = os.path.join(module_path, 'static', 'src', 'img', 'transparent_signature.png')
            if os.path.exists(signature_path):
                with open(signature_path, 'rb') as f:
                    signature_data = base64.b64encode(f.read()).decode('utf-8')
                return f"data:image/png;base64,{signature_data}"
        except Exception as e:
            _logger.error(f"Error loading signature: {e}")
        return None

    def _generate_html_content(self):
        """
        Generate HTML content for the report using Jinja2
        """
        from jinja2 import Environment, FileSystemLoader
        import os
        # إعداد Jinja2
        env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
        template = env.get_template('financial_claim_letter.html')
        company = self.env.company
        company_data = {
            'name': company.name,
            'logo': base64.b64encode(base64.b64decode(company.logo)).decode('utf-8') if company.logo else None,
            'address': company.partner_id.contact_address or 'غير محدد',
        }
        data = {
            'company': company_data,
            'partner_name': self.partner_id.name or 'غير محدد',
            'user_name': self.user_id.name or 'غير محدد',
            'date_order': self.date_order.strftime('%B %d, %Y') if self.date_order else 'غير محدد',
            'order_name': self.name or 'غير محدد',
        }

        # توليد الـ HTML
        html_content = template.render(**data)
        return html_content

    def _get_company_logo(self):
        """
        Get company logo as HTML <img> tag (Odoo 17)
        """
        try:
            company = self.env.company
            logo = company.logo

            if logo:
                if isinstance(logo, bytes):
                    logo_base64 = logo.decode('utf-8')
                else:
                    logo_base64 = logo

                return f'''
                    <img src="data:image/png;base64,{logo_base64}"
                         style="height: 160px; max-width: 300px; object-fit: contain;"/>
                '''
            else:
                return '''
                    <div style="height: 80px; width: 200px; background-color: #f9f9f9;
                                display: flex; align-items: center; justify-content: center;
                                border: 1px solid #ddd; border-radius: 6px; font-size: 10pt; color: #666;">
                        No Logo
                    </div>
                '''
        except Exception as e:
            _logger.error(f"Error processing company logo: {e}")
            return '''
                <div style="height: 80px; width: 200px; background-color: #f0f0f0;
                            display: flex; align-items: center; justify-content: center;
                            border: 1px solid #ddd; border-radius: 6px; font-size: 10pt; color: #666;">
                    Logo Error
                </div>
            '''

    def get_bg_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        company = self.env.company

        if company.id == 3:
            bg = "company_1.jpeg"
        elif company.id == 28:
            bg = "company_2.jpeg"
        elif company.id == 6:
            bg = "company_3.jpeg"
        else:
            bg = "default.jpeg"

        return f"{base_url}/collections_report/static/src/img/{bg}"

    def action_print_custom_pdf(self):
        """
        Generate Custom Financial Claim PDF using WeasyPrint
        """
        self.ensure_one()
        # Use due_date for header date
        header_dt = self.due_date or self.date or fields.Date.today()
        # Use date field for month_year in table
        dt = self.date or fields.Date.today()

        def _to_arabic_digits(s):
            arabic_nums = '٠١٢٣٤٥٦٧٨٩'
            return ''.join(arabic_nums[int(c)] if c.isdigit() else c for c in str(s))

        record_date = _to_arabic_digits(f"{header_dt.day} / {header_dt.month} / {header_dt.year}") + " م" if header_dt else ""
        record_number = self.name or ''

        month_year = babel.dates.format_date(dt, "MMMM yyyy", locale="ar")
        project_rows = ""
        row_count = 1
        detailed_projects = self.project_ids.filtered(lambda p: p.is_detailed)
        summary_projects = self.project_ids.filtered(lambda p: not p.is_detailed)

        for project in detailed_projects:
            project_rows += f"<tr><td style='border:1px solid #000; padding:3px;'>{row_count}</td><td style='border:1px solid #000; padding:3px; text-align:right;'>{project.support_type_id.name or project.project_id.name or ''} </td><td style='border:1px solid #000; padding:3px;'>{project.total_revenue:,.2f} ريال</td><td style='border:1px solid #000; padding:3px;'>{project.required_percent:,.2f} ريال</td></tr>"
            row_count += 1

        if summary_projects:
            sum_revenue = sum(summary_projects.mapped('total_revenue'))
            sum_required = sum(summary_projects.mapped('required_percent'))
            project_rows += f"<tr><td style='border:1px solid #000; padding:3px;'>{row_count}</td><td style='border:1px solid #000; padding:3px; text-align:right;'>المستحق عن شهر {month_year} م.</td><td style='border:1px solid #000; padding:3px;'>{sum_revenue:,.2f} ريال</td><td style='border:1px solid #000; padding:3px;'>{sum_required:,.2f} ريال</td></tr>"
            row_count += 1
        currency_symbol = self.currency_id.symbol
        total_revenue = round(sum(self.project_ids.mapped("total_revenue")), 2)
        required_percent = round(sum(self.project_ids.mapped('required_percent')) + sum(self.extra_amount_ids.mapped('amount')), 2)

        # Split amount into riyals and halalas
        riyals = int(required_percent)
        halalas = round((required_percent - riyals) * 100)

        # Convert to Arabic words
        riyals_text = num2words(riyals, lang='ar')
        required_percent_text = f"{riyals_text} ريال"

        if halalas > 0:
            halalas_text = num2words(halalas, lang='ar')
            required_percent_text += f" و {halalas_text} هللة"

        association_name = self.res_association_id.association_name
        assoc_data = self.res_association_id.x_studio_many2one_field_5j9_1j3lg5b21
        association = assoc_data.name if assoc_data else ""
        president_name = (assoc_data.chairman_name or '') if assoc_data else ""
        iban = (assoc_data.iban or "غير محدد") if assoc_data else "غير محدد"
        company_stamp = self._get_company_stamp_base64()
        signature = self._get_signature_base64()
        company = self.env.company

        company_logo = self._get_company_logo()
        company_name = company.name or ''
        company_street = company.street or ''
        company_city = company.city or ''
        company_phone = company.phone or ''
        company_email = company.email or ''
        bg_url = self.get_bg_url()

        # Get font paths for WeasyPrint
        font_ruqaa = self._get_font_path('Ruqaa.ttf') or '/collections_report/static/fonts/Ruqaa.ttf'
        font_amiri_regular = self._get_font_path(
            'Amiri/Amiri-Regular.ttf') or '/collections_report/static/fonts/Amiri/Amiri-Regular.ttf'
        font_amiri_bold = self._get_font_path(
            'Amiri/Amiri-Bold.ttf') or '/collections_report/static/fonts/Amiri/Amiri-Bold.ttf'
        font_amiri_italic = self._get_font_path(
            'Amiri/Amiri-Italic.ttf') or '/collections_report/static/fonts/Amiri/Amiri-Italic.ttf'
        font_amiri_bolditalic = self._get_font_path(
            'Amiri/Amiri-BoldItalic.ttf') or '/collections_report/static/fonts/Amiri/Amiri-BoldItalic.ttf'
        font_ibm_thin = self._get_font_path(
            'IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Thin.ttf') or '/collections_report/static/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Thin.ttf'
        font_ibm_extralight = self._get_font_path(
            'IBM_Plex_Sans_Arabic/IBMPlexSansArabic-ExtraLight.ttf') or '/collections_report/static/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-ExtraLight.ttf'
        font_ibm_light = self._get_font_path(
            'IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Light.ttf') or '/collections_report/static/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Light.ttf'
        font_ibm_regular = self._get_font_path(
            'IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Regular.ttf') or '/collections_report/static/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Regular.ttf'
        font_ibm_medium = self._get_font_path(
            'IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Medium.ttf') or '/collections_report/static/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Medium.ttf'
        font_ibm_semibold = self._get_font_path(
            'IBM_Plex_Sans_Arabic/IBMPlexSansArabic-SemiBold.ttf') or '/collections_report/static/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-SemiBold.ttf'
        font_ibm_bold = self._get_font_path(
            'IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Bold.ttf') or '/collections_report/static/fonts/IBM_Plex_Sans_Arabic/IBMPlexSansArabic-Bold.ttf'
        font_katibeh = self._get_font_path(
            'Katibeh/Katibeh-Regular.ttf') or '/collections_report/static/fonts/Katibeh/Katibeh-Regular.ttf'
        font_tajawal_extralight = self._get_font_path(
            'Tajawal/Tajawal-ExtraLight.ttf') or '/collections_report/static/fonts/Tajawal/Tajawal-ExtraLight.ttf'
        font_tajawal_light = self._get_font_path(
            'Tajawal/Tajawal-Light.ttf') or '/collections_report/static/fonts/Tajawal/Tajawal-Light.ttf'
        font_tajawal_regular = self._get_font_path(
            'Tajawal/Tajawal-Regular.ttf') or '/collections_report/static/fonts/Tajawal/Tajawal-Regular.ttf'
        font_tajawal_medium = self._get_font_path(
            'Tajawal/Tajawal-Medium.ttf') or '/collections_report/static/fonts/Tajawal/Tajawal-Medium.ttf'
        font_tajawal_bold = self._get_font_path(
            'Tajawal/Tajawal-Bold.ttf') or '/collections_report/static/fonts/Tajawal/Tajawal-Bold.ttf'
        font_tajawal_extrabold = self._get_font_path(
            'Tajawal/Tajawal-ExtraBold.ttf') or '/collections_report/static/fonts/Tajawal/Tajawal-ExtraBold.ttf'
        font_tajawal_black = self._get_font_path(
            'Tajawal/Tajawal-Black.ttf') or '/collections_report/static/fonts/Tajawal/Tajawal-Black.ttf'
        font_liftaswashfixed = self._get_font_path(
            'alfont_com_Liftaswashfixed-Regular.otf') or '/collections_report/static/fonts/alfont_com_Liftaswashfixed-Regular.otf'

        # Generate HTML
        html_code = f"""
              <!DOCTYPE html>
            <html lang="ar" dir="rtl"> 
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&amp;display=swap" rel="stylesheet">
                            <style>
            @page {{
                        size: A4 portrait;
                        margin: 4cm 0.5cm 2.5cm 0.5cm;
                    }}

                    .page-bg {{
                        position: fixed;
                        top: -5cm;
                        left: -0.5cm;
                        right: -0.5cm;
                        bottom: -5cm;
                        z-index: -1;
                    }}
                    .page-bg img {{
                        width: 100%;
                        height: 100%;
                        display: block;
                    }}

                    .content {{
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Cairo', Arial, sans-serif;
                    font-size: 11pt;
                    line-height: 1.5;
                }}

                body {{
                    font-family: 'Cairo', Arial, sans-serif;
                    font-size: 11pt;
                    line-height: 1.4;
                    color: #333;
                    margin: 0;
                    padding: 0 0.5cm;
                    direction: rtl;
                    text-align: right;
                }}
                    .container {{
                        max-width: 100%;
                        margin: 0 auto;
                        padding: 0 15px;
                    }}

                    /* ستايلات الـ Header المستخرجة */
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-start;
                        margin-bottom: 25px;
                        border-bottom: 2px solid #D4AF37;
                        padding-bottom: 10px;

                    }}

                    .company-info {{
                        display: flex;
                        align-items: flex-start;
                        gap: 20px;
                    }}

                    .logo-section {{
                        flex-shrink: 0;
                    }}

                    .company-details {{
                        flex-grow: 1;
                    }}

                    .company-details h1 {{
                        color: #D4AF37;
                        margin: 0 0 10px 0;
                        font-size: 24pt;
                    }}

                    .company-info p {{
                        margin: 5px 0;
                        font-size: 10pt;
                        color: #666;
                    }}

                    .report-title {{
                        text-align: right;
                    }}

                    .report-title h2 {{
                        color: #D4AF37;
                        margin: 0 0 5px 0;
                        font-size: 14pt;
                        white-space: nowrap;
                    }}

                    .report-title h3 {{
                        color: #666;
                        margin: 0;
                        font-size: 16pt;
                    }}

                    .header-info {{
                        margin-top: 10px;
                        font-size: 10pt;
                    }}

                    .info-row {{
                        margin: 3px 0;
                        margin-top: 40px;
                        display: flex;
                        gap: 30px;
                        justify-content: center;
                        align-items: right;
                        text-align: right;
                    }}

                    .info-item {{
                        display: inline-block;
                    }}

                    .info-row span {{
                        white-space: nowrap;
                        margin-left: 20px;
                    }}

                    .info-item.empty-row {{
                        display: block;   /* forces line break */
                        height: 20px;     /* adjust for how much space you want */
                        content: "";      /* ensures it's treated as empty */
                    }}


                .title-row {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-size: 20px;
                    font-weight: bold;
                    font-family: 'Cairo', Arial, sans-serif;
                }}
                .title-row .right {{
                    text-align: right;
                }}
                .title-row .left {{
                    text-align: left;
                }}
                    .salam {{
                    width: 150px;
                    height: auto;
                    margin: 10px 0;
                }}

                @font-face {{
                    font-family: 'Ruqaa';
                    src: url('{font_ruqaa}') format('truetype');
                }}

                /* Amiri Font */
                @font-face {{
                    font-family: 'Amiri';
                    src: url('{font_amiri_regular}') format('truetype');
                    font-weight: 400;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Amiri';
                    src: url('{font_amiri_bold}') format('truetype');
                    font-weight: 700;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Amiri';
                    src: url('{font_amiri_italic}') format('truetype');
                    font-weight: 400;
                    font-style: italic;
                }}
                @font-face {{
                    font-family: 'Amiri';
                    src: url('{font_amiri_bolditalic}') format('truetype');
                    font-weight: 700;
                    font-style: italic;
                }}

                /* IBM Plex Sans Arabic Font */
                @font-face {{
                    font-family: 'IBM Plex Sans Arabic';
                    src: url('{font_ibm_thin}') format('truetype');
                    font-weight: 100;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'IBM Plex Sans Arabic';
                    src: url('{font_ibm_extralight}') format('truetype');
                    font-weight: 200;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'IBM Plex Sans Arabic';
                    src: url('{font_ibm_light}') format('truetype');
                    font-weight: 300;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'IBM Plex Sans Arabic';
                    src: url('{font_ibm_regular}') format('truetype');
                    font-weight: 400;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'IBM Plex Sans Arabic';
                    src: url('{font_ibm_medium}') format('truetype');
                    font-weight: 500;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'IBM Plex Sans Arabic';
                    src: url('{font_ibm_semibold}') format('truetype');
                    font-weight: 600;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'IBM Plex Sans Arabic';
                    src: url('{font_ibm_bold}') format('truetype');
                    font-weight: 700;
                    font-style: normal;
                }}

                /* Katibeh Font */
                @font-face {{
                    font-family: 'Katibeh';
                    src: url('{font_katibeh}') format('truetype');
                    font-weight: 400;
                    font-style: normal;
                }}

                /* Tajawal Font */
                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_tajawal_extralight}') format('truetype');
                    font-weight: 200;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_tajawal_light}') format('truetype');
                    font-weight: 300;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_tajawal_regular}') format('truetype');
                    font-weight: 400;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_tajawal_medium}') format('truetype');
                    font-weight: 500;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_tajawal_bold}') format('truetype');
                    font-weight: 700;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_tajawal_extrabold}') format('truetype');
                    font-weight: 800;
                    font-style: normal;
                }}
                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_tajawal_black}') format('truetype');
                    font-weight: 900;
                    font-style: normal;
                }}

                /* Liftaswashfixed Font */
                @font-face {{
                    font-family: 'Liftaswashfixed';
                    src: url('{font_liftaswashfixed}') format('opentype');
                    font-weight: 400;
                    font-style: normal;
                }}

                .ruqaa {{
                    font-family: 'Cairo', sans-serif;
                }}
                .amiri {{
                    font-family: 'Amiri', serif;
                }}
                .ibm-plex-sans-arabic {{
                    font-family: 'IBM Plex Sans Arabic', sans-serif;
                }}
                .katibeh {{
                    font-family: 'Katibeh', serif;
                }}
                .tajawal {{
                    font-family: 'Cairo', sans-serif;
                }}
                .liftaswashfixed {{
                    font-family: 'Liftaswashfixed', sans-serif;
                }}

                        .stamp {{
                           margin-top: 20px;
                         }}
                         .stamp img {{
                           width: 120px;
                           height: 120px;
                           object-fit: contain;   
                           border-radius: 60%;    
                           border: 3px solid #ddd; 
                           padding: 5px;           
                           background: #fff;   
                           margin-bottom: 10px;
                         }}

                    .header-date-number {{
                        position: fixed;
                        top: -3cm;
                        left: 1.5cm;
                        font-size: 14px;
                        font-weight: bold;
                        line-height: 1.4;
                        z-index: 10;
                    }}
                    .header-date-number .header-number-value {{
                        margin-top: 0.2cm;
                    }}

                </style>
            </head>
            <body>
                    <div class="page-bg"><img src="{bg_url}" /></div>
                    <div class="header-date-number">
                       <div class="header-date-value">{record_date}</div>
                       <div class="header-number-value">{record_number}</div>
                    </div>
                    <div class="content">
                       <div class="title-row">
                          <span class="right">سعادة رئيس/{association_name}</span>
                          <span class="left">سلمه الله</span>
                        </div>
                      <div class="ruqaa" style="display:flex; justify-content:center; font-size:20px;">
                            <span style="margin-left:40px;">السلام عليكم ورحمه الله وبركاته</span>
                            <span style="margin-right:40px;">تحيه طيبه وبعد</span>
                        </div>
                        <div style="text-align:center; margin-top:4px; font-family: 'Cairo', Arial, sans-serif;">
                            <p style="margin-top:5px; font-size:14px; line-height:1.5; direction:rtl; font-weight: bold; text-align:right;">
                                وإشارة للعقد المبرم مع جمعيتكم المباركة نأمل التكرم بصرف المستحق ل{company_name} عن
                                الخدمات التسويقية المقدمة، التفاصيل كالتالي:
                            </p>
                        </div>
                        <table style="width:100%; border-collapse:collapse; margin-top:8px; font-size:13px; direction:rtl; text-align:center; font-family: 'Cairo', Arial, sans-serif;">
                            <thead>
                                <tr style="background:#f0f0f0;">
                                    <th style="border:1px solid #000; padding:3px; width:5%;">م</th>
                                    <th style="border:1px solid #000; padding:3px; width:45%;">البيـــان</th>
                                    <th style="border:1px solid #000; padding:3px; width:25%;">اجمالي الايرادات</th>
                                    <th style="border:1px solid #000; padding:3px; width:25%;">المبلغ المستحق</th>
                                </tr>
                            </thead>
                                <tbody>
                                {project_rows}
                                {"".join([f'<tr><td style="border:1px solid #000; padding:3px;">{row_count + i}</td><td style="border:1px solid #000; padding:3px; text-align:right;">{ea.description}</td><td style="border:1px solid #000; padding:3px;">-</td><td style="border:1px solid #000; padding:3px;">{ea.amount:,.2f} ريال</td></tr>' for i, ea in enumerate(self.extra_amount_ids)])}
                                     <tr style="background:#f0f0f0;">
                                        <th style="border:1px solid #000; padding:3px;"></th>
                                        <th style="border:1px solid #000; padding:3px; width:45%;">الاجمالي شامل الضريبة</th>
                                        <td colspan="2" style="border:1px solid #000; padding:3px; text-align:center;">
                                            {required_percent:,.2f} ريال
                                        </td>
                                </tr>
                                <tr>
                                      <td colspan="4" style="border:1px solid #000; padding:3px; text-align:right;">
                                        {required_percent_text}
                                    </td>  
                                </tr>
                            </tbody>
                        </table>
                        <!-- تجميع كل المحتوى من الملاحظة إلى التوقيع في حاوية واحدة لمنع الانقسام -->
                        <div style="page-break-inside: avoid;">
                            <div style="margin-top:8px;">
                                <p style="margin:0; font-size:14px; direction:rtl; text-align:right; font-family: 'Cairo', Arial, sans-serif; font-weight:bold;">
                                    ملاحظة/ يلزم الرد باعتماد مبلغ المطالبة لاصدار الفاتورة الالكترونية
                                </p>
                            </div>
                            <div style="margin-top:3px;">
                                <p style="margin-top:5px; font-size:14px; line-height:1.5; direction:rtl; text-align:right; font-family: 'Cairo', Arial, sans-serif;">
                                 نأمل اصدار الشيك باسم/ {association} أو التحويل على حساب الشركة بمصرف الراجحي رقم ({iban}) 
                                </p>
                            </div>    
                            <div style="margin-top:3px;">
                                <p class="ruqaa" style="margin-top:5px; font-size:20px; line-height:1.4; direction:rtl; text-align:center;">
                                    ولكم جزيـل الشكر والتقدير...
                                </p>
                            </div>

                            <!-- سكشن رئيس مجلس الإدارة مع الختم - موضوع على اليسار بدون position:absolute -->
                            <div style="margin-top:20px; text-align:left; font-family: 'Cairo', Arial, sans-serif;">
                                <table border="0" cellpadding="0" cellspacing="0" style="display:inline-table; text-align:center; border-collapse:collapse;">
                                    <tr>
                                        <td style="vertical-align:bottom; padding:0 10px; text-align:center;">
                                            <p style="margin:0 0 5px 0; font-size:20px; font-weight:bold;">رئيس مجلس الإدارة</p>
                                            <div style="margin:5px 0;">
                                                <img src="{signature}" style="width:200px; height:auto; max-height:80px;"/>
                                            </div>
                                            <p style="margin:5px 0 0 0; font-size:20px; font-weight:bold;">{president_name}</p>
                                        </td>
                                        <td style="vertical-align:middle; padding:0 10px;">
                                            <div class="stamp" style="opacity:0.9;">
                                                <img src="{company_stamp}" style="width:120px; height:120px; object-fit:contain;"/>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                     </div>
            </body>
            </html>
        """

        try:
            # ✅ Generate PDF
            pdf_content = HTML(
                string=html_code,
                base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            ).write_pdf()

            # ✅ Save attachment
            attachment = self.env['ir.attachment'].create({
                'name': f"Financial-Claim-.pdf",
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': self._name,  # dynamic instead of hardcoded
                'res_id': self.id,
                'mimetype': 'application/pdf'
            })

            # ✅ Return download action
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'new',
            }

        except Exception as e:
            _logger.error(f"Error generating PDF: {e}")
            raise UserError(_("Failed to generate PDF: %s") % e)
