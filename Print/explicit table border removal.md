# Explicit Table Border Removal (Header/Footer Only)

## Goal
Remove borders **only** from the custom header and footer tables in the `invoice_report` module, without affecting body tables (invoice lines, totals, buyer table).

## Why borders were still visible
In Odoo PDF reports, borders can come from multiple layers:

1. Odoo report layout styles (`o_table_*`, `o_footer_content`, layout wrappers)
2. Pseudo-elements (`::before`, `::after`) used by some table/layout styles
3. Parent header/footer containers in `web.external_layout_standard`
4. wkhtmltopdf rendering quirks (where `border: none` alone is sometimes not enough)

## What we changed

### 1) Scope border removal to header/footer wrappers only
We wrapped only header/footer content in dedicated classes:
- `.inv-header-clean`
- `.inv-footer-clean`

Then we targeted all relevant descendants + pseudo-elements:

```css
.inv-header-clean,
.inv-header-clean::before,
.inv-header-clean::after,
.inv-header-clean table,
.inv-header-clean table::before,
.inv-header-clean table::after,
.inv-header-clean tbody,
.inv-header-clean tbody::before,
.inv-header-clean tbody::after,
.inv-header-clean tr,
.inv-header-clean tr::before,
.inv-header-clean tr::after,
.inv-header-clean td,
.inv-header-clean td::before,
.inv-header-clean td::after,
.inv-footer-clean,
.inv-footer-clean::before,
.inv-footer-clean::after,
.inv-footer-clean table,
.inv-footer-clean table::before,
.inv-footer-clean table::after,
.inv-footer-clean tbody,
.inv-footer-clean tbody::before,
.inv-footer-clean tbody::after,
.inv-footer-clean tr,
.inv-footer-clean tr::before,
.inv-footer-clean tr::after,
.inv-footer-clean td,
.inv-footer-clean td::before,
.inv-footer-clean td::after {
    border: none !important;
    border-width: 0 !important;
    border-style: none !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

.inv-header-clean::before,
.inv-header-clean::after,
.inv-footer-clean::before,
.inv-footer-clean::after,
.inv-header-clean table::before,
.inv-header-clean table::after,
.inv-footer-clean table::before,
.inv-footer-clean table::after {
    content: none !important;
    display: none !important;
}
```

### 2) Opt out of Odoo automatic table styling
Both header/footer tables use:

```xml
<table class="o_ignore_layout_styling table-borderless"
       border="0" cellpadding="0" cellspacing="0"
       frame="void" rules="none"
       style="border:none !important; border-color:transparent !important; border-collapse:collapse !important; border-spacing:0 !important; ...">
```

Notes:
- `o_ignore_layout_styling` prevents Odoo table decorators (`table:not(.o_ignore_layout_styling)` rules).
- `table-borderless` adds another defensive layer for PDF CSS.
- `frame="void" rules="none"` helps wkhtmltopdf ignore table frame/grid borders.

### 3) Add inline no-border fallback on every row/cell
For stubborn PDF rendering, each `tr`/`td` in header/footer gets explicit no-border styles:

```xml
<tr style="border:none !important; border-color:transparent !important; ...">
    <td style="border:none !important; border-color:transparent !important; ...">...</td>
</tr>
```

### 4) Strip borders from parent layout containers (critical)
In `invoice_external_layout_standard_overrides`, we also remove border styles from parent containers:

```xml
<xpath expr="//div[contains(@t-attf-class, 'header')]" position="attributes">
    <attribute name="t-attf-style">
        #{invoice_report_show_footer and '... border:none !important; border-color:transparent !important; ...' or ''}
    </attribute>
</xpath>

<xpath expr="//div[contains(@t-attf-class, 'footer o_company_')]" position="attributes">
    <attribute name="t-attf-style">
        #{invoice_report_show_footer and '... border:none !important; border-color:transparent !important; ...' or ''}
    </attribute>
</xpath>

<xpath expr="//div[contains(@class, 'o_footer_content')]" position="replace">
    <div t-if="invoice_report_show_footer" class="o_footer_content pt-1"
         style="... border:none !important; border-color:transparent !important; ...">
        <t t-call="invoice_report.invoice_report_footer_content"/>
    </div>
</xpath>
```

This prevented inherited border lines from reappearing around custom borderless tables.

## Why this was safe
- Border removal was **limited to header/footer classes only**.
- Main report tables (`.inv-grid`, `.inv-lines`, totals, buyer info) kept their borders and spacing.
- No global table reset was applied to the whole report.

## Validation checklist
After changes:
1. Update module `invoice_report`
2. Regenerate PDF
3. Confirm:
   - Header/footer outer borders are gone
   - Body tables still have their intended borders
   - Page number and footer content still render correctly

## File reference
Implementation lives in:
- `/Volumes/Samsung T5/Odoo/Odoo/G/18/atheer/Atheer-Production/invoice_report/report/invoice_report.xml`
