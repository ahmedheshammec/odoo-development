# Two-pass PDF rendering to inject total page count in report body

## Goal
Insert the total number of pages into the body of a QWeb PDF report (not the footer)
without affecting other reports.

## Problem
wkhtmltopdf only knows the total pages at render time. If the page count is not in
the footer/header, you cannot access it directly in the report body.

## Approach (two-pass render)
Render the report twice:
1) First pass: generate a temporary PDF and count its pages.
2) Second pass: re-render the report with `total_pages` injected into context.

This keeps the behavior of a normal print action but adds a small extra render
for only the target report.

## Implementation in this module
Location: `reports/agreement_report.py`

### 1) Extend `ir.actions.report` and override `_render_qweb_pdf`
```python
# reports/agreement_report.py
import io
import logging

from odoo import models
from odoo.tools.pdf import PdfReader

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _count_pages(self, pdf_content):
        try:
            reader = PdfReader(io.BytesIO(pdf_content))
            return len(reader.pages)
        except Exception as exc:
            _logger.warning("Unable to count pages for agreement report: %s", exc)
            return 0

    def _render_qweb_pdf(self, report_ref=None, docids=None, data=None):
        target_name = report_ref or (len(self) == 1 and self.report_name)
        is_agreement = target_name == "print_papers.report_agreement_document"
        if is_agreement and not self.env.context.get("skip_agreement_two_pass"):
            # First pass: get PDF and count pages
            first_pdf, first_format = super()._render_qweb_pdf(report_ref, docids, data=data)
            total_pages = self._count_pages(first_pdf)

            # Second pass: inject total_pages, avoid re-entry
            final_pdf, final_format = super(
                IrActionsReport,
                self.with_context(skip_agreement_two_pass=True, total_pages=total_pages),
            )._render_qweb_pdf(report_ref, docids, data=data)
            return final_pdf, final_format

        return super()._render_qweb_pdf(report_ref, docids, data=data)
```

Key points:
- `is_agreement` targets a single report by `report_name`. This isolates the logic
  so other reports are unaffected.
- `skip_agreement_two_pass` prevents infinite recursion on the second render.
- The "temporary PDF" never touches disk; it is in-memory only.

### 2) Use the injected value in QWeb template body
Location: `reports/agreement_report.xml`
```xml
<div style="text-align: center; line-height: 1.8;">
    تم إعداد هذه الاتفاقية من نسختين وعدد
    (
    <t t-esc="env.context.get('total_pages', '')"/>
    )
    صفحات
    لكل عقد ويُسلم كل طرف نسخة منها
</div>
```

The `total_pages` key is read from context and can be placed anywhere in the body.

## How to adapt this for another report
1) Pick the report action `report_name` of your target report.
2) Add a dedicated condition (like `is_agreement`) in `_render_qweb_pdf`.
3) Use a unique context flag (like `skip_<report>_two_pass`) to prevent recursion.
4) Reference `env.context.get('total_pages')` in the QWeb body.

Example for a different report:
```python
target_name = report_ref or (len(self) == 1 and self.report_name)
is_target = target_name == "your_module.report_my_document"
if is_target and not self.env.context.get("skip_my_report_two_pass"):
    ...
    return super(
        IrActionsReport,
        self.with_context(skip_my_report_two_pass=True, total_pages=total_pages),
    )._render_qweb_pdf(...)
```

## Notes and caveats
- This method adds one extra render for the target report only, so it is slightly
  slower but stays transparent to users.
- If counting pages fails, `total_pages` defaults to `0` (see `_count_pages`).
- The injection happens purely via context; no changes to report action are needed.
