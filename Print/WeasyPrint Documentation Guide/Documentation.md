# WeasyPrint Documentation Guide for Odoo 17

## Purpose

This guide documents the custom WeasyPrint-based PDF pattern used in the `collections_report` module. It is intended to be reusable when you need to build a similar PDF report for a new model, a new database, or a new custom addon.

This is not the standard Odoo report flow. Instead of:

- `ir.actions.report`
- a QWeb XML template
- the regular Odoo PDF rendering pipeline

this pattern does the following:

1. Adds a button to a form view.
2. Calls a Python object method with `type="object"`.
3. Builds a full HTML document as a Python string.
4. Uses `WeasyPrint` to convert the HTML to PDF.
5. Saves the PDF as an `ir.attachment`.
6. Returns an `ir.actions.act_url` so the user downloads the generated file.

This approach gives strong control over layout and styling, but it is less standard and harder to maintain than Odoo QWeb reports.

## Reference Module

The implementation documented here comes from:

- Module: `collections_report`
- Model: `collections.collections`
- Button method: `action_print_custom_pdf`

Primary reference file included in this guide folder:

- `references/collections_collections.py`

## Folder Contents

This guide folder is expected to contain:

- `Documentation.md`
- `references/collections_collections.py`
- `references/collections_view.xml`
- `assets/fonts.tar.gz`
- `assets/images.tar.gz`

The archives are included so the guide remains portable without creating dozens of loose files.

## When To Use This Pattern

Use WeasyPrint when:

- the PDF requires very custom page layout
- the report needs print-heavy CSS and fixed-position elements
- background images and typography need tighter control
- QWeb plus the standard report flow becomes too restrictive

Do not default to this pattern when:

- a normal business report can be handled by QWeb
- inheritance and maintainability matter more than layout flexibility
- multiple developers will maintain the report long-term

## High-Level Architecture

The full request flow is:

1. User opens the target record form.
2. User clicks the custom print button.
3. The form button calls a model method.
4. The method collects data from the record and related models.
5. The method prepares helper assets:
   - base64 signature
   - base64 stamp
   - file URLs for font files
   - background image URL
6. The method builds HTML and CSS inline.
7. `WeasyPrint.HTML(...).write_pdf()` renders the PDF binary.
8. An attachment is created in `ir.attachment`.
9. Odoo returns a download URL for the attachment.

## Core Building Blocks

### 1. View Button

The report is exposed from XML using a form button:

```xml
<button name="action_print_custom_pdf"
        string="خطاب مطالبه مالية"
        type="object"
        icon="fa-print"
        class="btn-primary"/>
```

Important points:

- `name` must match the Python method name.
- `type="object"` means Odoo calls a model method on the current record.
- if the report should be restricted, use `groups`.

### 2. Python Entry Point

The report entry point looks like:

```python
def action_print_custom_pdf(self):
    self.ensure_one()
```

Important points:

- `self.ensure_one()` is recommended because the HTML is usually built for one record at a time.
- The method is responsible for both data preparation and PDF generation.

### 3. Helper Methods

This implementation uses helper methods for:

- `_get_company_stamp_base64()`
- `_get_font_path(font_file)`
- `_get_signature_base64()`
- `_get_company_logo()`
- `get_bg_url()`

These helpers keep the main method shorter and isolate repeated logic.

### 4. HTML Generation

The implementation creates a full HTML document with inline CSS:

```python
html_code = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4 portrait; margin: 4cm 0.5cm 2.5cm 0.5cm; }
    </style>
</head>
<body>
    ...
</body>
</html>
"""
```

Important points:

- Arabic reports should use `dir="rtl"`.
- `@page` is important for margins and paper size.
- inline CSS makes the document self-contained.
- Python f-strings inject dynamic values directly into the HTML.

### 5. PDF Rendering

The actual render call is:

```python
pdf_content = HTML(
    string=html_code,
    base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
).write_pdf()
```

Important points:

- `string=html_code` renders the HTML you generated in Python.
- `base_url` helps resolve URLs used in the HTML.
- local fonts in this module are loaded using `file://` paths, not only HTTP URLs.

### 6. Attachment Creation and Download

The rendered PDF is saved and returned:

```python
attachment = self.env['ir.attachment'].create({
    'name': 'Financial-Claim-.pdf',
    'type': 'binary',
    'datas': base64.b64encode(pdf_content),
    'res_model': self._name,
    'res_id': self.id,
    'mimetype': 'application/pdf',
})

return {
    'type': 'ir.actions.act_url',
    'url': f'/web/content/{attachment.id}?download=true',
    'target': 'new',
}
```

This is why there is no `ir.actions.report` record involved in this report.

## Prerequisites

### Python Dependencies

At minimum, this pattern depends on:

```python
import base64
import os
import babel.dates
from num2words import num2words
from weasyprint import HTML
from odoo import models, fields, _
from odoo.exceptions import UserError
```

You need the following Python packages installed in the Odoo environment:

- `weasyprint`
- `babel`
- `num2words`

Depending on your environment, WeasyPrint may also require system libraries for text shaping and image rendering. If WeasyPrint import or PDF generation fails on a new server, check the OS-level dependencies first.

### Odoo Dependencies

Your custom module should declare any business module dependencies that provide:

- the target model
- the form view you inherit
- any related fields used in the report

Example:

```python
'depends': ['base', 'managing_association_contracts']
```

### Data Prerequisites

Before this report can render correctly, the source record usually needs:

- a valid current company
- related association data
- partner and project lines
- any extra amount lines
- a signature image if one is expected
- a company stamp if one is expected
- the date fields used in the header and table

### Static Assets

This specific implementation uses:

- multiple Arabic fonts
- background image templates
- a transparent signature image

If you move the implementation to another module, keep the static paths aligned with the new module name.

## Static Asset Strategy

### Fonts

The implementation resolves fonts from the module itself:

```python
module_path = os.path.dirname(os.path.dirname(__file__))
font_path = os.path.join(module_path, 'static', 'fonts', font_file)
return f"file://{font_path}"
```

This is a good pattern because:

- it avoids depending on system fonts
- it makes the report more portable across environments
- it keeps Arabic typography predictable

### Images

There are two image strategies in the reference implementation:

1. Dynamic binary fields converted to base64:
   - company stamp
   - signature image loaded from file and converted to base64
2. Background image served from module static files:
   - company-specific page background

The `get_bg_url()` method chooses a background image based on company ID. That means moving this report to a new database may require adjusting:

- company IDs
- file names
- default behavior

## What Makes This Report Custom

This report does several non-standard things:

- it injects the entire HTML document in Python
- it manually formats Arabic dates
- it manually converts digits to Arabic numerals
- it manually converts amounts to Arabic words
- it manually concatenates table rows as HTML strings
- it does not use QWeb inheritance
- it does not use `ir.actions.report`

These choices increase control, but they also make refactoring harder.

## Reusable Implementation Template

Use this as a cleaner starting point for a new model:

```python
import base64
import os
import logging

from weasyprint import HTML
from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MyModel(models.Model):
    _inherit = 'your.model'

    def _get_font_path(self, font_file):
        module_path = os.path.dirname(os.path.dirname(__file__))
        font_path = os.path.join(module_path, 'static', 'fonts', font_file)
        if os.path.exists(font_path):
            return f"file://{font_path}"
        return None

    def _build_report_html(self):
        self.ensure_one()
        title = self.display_name or ''
        font_regular = self._get_font_path('Tajawal/Tajawal-Regular.ttf')

        return f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4 portrait;
                    margin: 2cm;
                }}

                @font-face {{
                    font-family: 'Tajawal';
                    src: url('{font_regular}') format('truetype');
                }}

                body {{
                    font-family: 'Tajawal', sans-serif;
                    direction: rtl;
                    text-align: right;
                }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <p>Custom WeasyPrint report.</p>
        </body>
        </html>
        """

    def action_print_my_weasy_pdf(self):
        self.ensure_one()
        html_code = self._build_report_html()
        try:
            pdf_content = HTML(
                string=html_code,
                base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            ).write_pdf()

            attachment = self.env['ir.attachment'].create({
                'name': f'{self._name}-{self.id}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': self._name,
                'res_id': self.id,
                'mimetype': 'application/pdf',
            })

            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'new',
            }
        except Exception as e:
            _logger.exception('Failed to generate WeasyPrint PDF')
            raise UserError(_('Failed to generate PDF: %s') % e)
```

## XML Template For A New Button

Use this in your form inheritance:

```xml
<record id="view_form_inherit_my_weasy_report" model="ir.ui.view">
    <field name="name">your.model.form.inherit.weasy.report</field>
    <field name="model">your.model</field>
    <field name="inherit_id" ref="your_module.original_form_view"/>
    <field name="arch" type="xml">
        <xpath expr="//header" position="inside">
            <button name="action_print_my_weasy_pdf"
                    string="Print PDF"
                    type="object"
                    class="btn-primary"
                    icon="fa-print"/>
        </xpath>
    </field>
</record>
```

## Recommended Folder Structure For New Modules

If you build a new WeasyPrint report module, use a structure like this:

```text
my_weasy_report/
|-- __init__.py
|-- __manifest__.py
|-- models/
|   |-- __init__.py
|   `-- my_model.py
|-- views/
|   `-- my_model_views.xml
`-- static/
    |-- fonts/
    |   `-- ...
    `-- src/
        `-- img/
            `-- ...
```

This keeps Python, views, fonts, and images in predictable places.

## Recommended Refactor Pattern

If you continue using WeasyPrint, this is the better structure:

1. Keep button logic in XML.
2. Keep data preparation in Python helper methods.
3. Move HTML to a dedicated template file.
4. Render that template from Python.
5. Keep fonts and images under `static/`.

That gives you most of the flexibility of WeasyPrint without making the Python method unreadable.

## Option: Use Jinja2 Instead Of Inline HTML

The reference file already contains a partial Jinja2 idea:

```python
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
template = env.get_template('financial_claim_letter.html')
html_content = template.render(**data)
```

However, in the current module there is no corresponding template file shipped with the implementation that the active button uses. The real report is still built inline in Python.

If you want a maintainable WeasyPrint setup, Jinja2 or QWeb-generated HTML is a better direction than a giant inline f-string.

## Arabic and RTL Considerations

For Arabic reports, validate all of the following:

- `dir="rtl"` on the HTML root
- `text-align: right` where appropriate
- fonts that actually support Arabic glyphs
- date formatting using Arabic locale where needed
- amount-to-words conversion in Arabic
- digit replacement if the business wants Arabic numerals

The reference report explicitly does all of that.

Example Arabic digit conversion:

```python
def _to_arabic_digits(s):
    arabic_nums = '٠١٢٣٤٥٦٧٨٩'
    return ''.join(arabic_nums[int(c)] if c.isdigit() else c for c in str(s))
```

## Common Pitfalls

### 1. Hardcoded Company IDs

This implementation selects backgrounds using company IDs:

- `3`
- `28`
- `6`

That is fragile across databases. In a new database, those IDs may not match the same companies.

Better alternatives:

- use a field on `res.company`
- use XML IDs
- use a configurable parameter

### 2. Inline HTML String Size

A large HTML string in Python becomes difficult to:

- review
- debug
- translate
- inherit
- reuse

### 3. Missing Static Files

If fonts or images are missing after migration, the PDF may:

- render with broken typography
- lose Arabic shaping quality
- miss signature or background
- fail to load local assets

### 4. Broken Binary Fields

If stamp or signature data is empty, the generated HTML may render missing images. Add fallbacks where necessary.

### 5. Environment Setup

A report can work in one server and fail in another if WeasyPrint or its system libraries are not installed correctly.

## Migration Checklist For A New DB Or Model

Use this checklist when reusing the pattern:

1. Confirm the target model and form view.
2. Add the custom button in an inherited XML view.
3. Create the Python method on the target model.
4. Install `weasyprint`, `babel`, and `num2words` in the environment.
5. Copy required fonts into the new module `static/fonts/`.
6. Copy required images into `static/src/img/`.
7. Replace hardcoded model-specific field names.
8. Replace hardcoded company IDs and business logic.
9. Verify Arabic locale formatting on the target server.
10. Test with real record data.
11. Confirm the attachment download works.
12. Confirm permissions for the users who can print.

## Debugging Guide

When the PDF fails, debug in this order:

### Import Errors

Check whether Odoo can import:

- `weasyprint`
- `babel`
- `num2words`

### Asset Paths

Check:

- `file://` font paths
- static image paths
- existence of local files on disk

### Data Integrity

Check whether the record has:

- required dates
- related association data
- project lines
- stamp or signature content

### HTML Content

A practical debugging trick is to temporarily save the generated HTML to a file so you can inspect it before PDF rendering.

### Odoo Log Output

The method already catches exceptions and raises a `UserError`. For deeper debugging, check the actual server log for the original exception.

## Suggested Best Practices

If you implement another report with this style, prefer these rules:

- Keep the button method thin.
- Move row-building to helper methods.
- Move HTML to a template file.
- Keep all paths module-relative.
- Avoid hardcoded database IDs.
- Keep image data handling defensive.
- Use attachment names that identify the record clearly.
- Use one font family unless multiple families are truly necessary.

## What To Reuse From This Reference

Good parts worth reusing:

- helper method for local font resolution
- helper method for binary-to-base64 image conversion
- `ensure_one()`
- attachment-based download flow
- Arabic formatting helpers

Parts worth improving before reuse:

- inline HTML size
- hardcoded company IDs
- mixed business logic and presentation
- unused helper/template path hints
- duplicated logic across multiple report methods

## Included Reference Assets

The accompanying archives contain the assets referenced by the current implementation:

- `assets/fonts.tar.gz`
- `assets/images.tar.gz`

The `references/` folder contains the source references:

- `references/collections_collections.py`
- `references/collections_view.xml`

## Final Recommendation

If your goal is maintainability inside Odoo, prefer QWeb unless the report genuinely needs WeasyPrint-level layout control.

If your goal is maximum PDF layout control and you accept a more custom implementation, use WeasyPrint but structure it better than the current example:

- Python for data
- template file for HTML
- module static files for assets
- attachment download at the end

That is the best compromise for future reuse.
