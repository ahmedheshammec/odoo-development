# Fixing Table Column Widths in Odoo 18 PDF Reports

A comprehensive guide to controlling table column widths in Odoo 18 reports when wkhtmltopdf ignores your CSS.

---

## Table of Contents

1. [The Problem](#the-problem)
2. [Root Cause Analysis](#root-cause-analysis)
3. [What Didn't Work](#what-didnt-work)
4. [The Solution](#the-solution)
5. [Removing Unwanted Borders](#removing-unwanted-borders)
6. [Complete Working Example](#complete-working-example)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)

---

## The Problem

When customizing Odoo 18 report tables (like Sale Order reports), you may need to:
- Add custom columns (e.g., Internal Ref, Lot/Serial Number, Expiration Date)
- Control column widths to make certain columns wider than others
- Ensure the layout looks correct in **both HTML preview AND PDF output**

The frustrating issue: **Your column widths work perfectly in HTML view but are completely ignored in PDF output**, resulting in evenly distributed columns regardless of your CSS.

### Symptoms
- HTML report (`/report/html/...`) shows correct column widths
- PDF report (`/report/pdf/...`) shows all columns with equal width
- No matter what CSS you apply, PDF column widths don't change

---

## Root Cause Analysis

### 1. wkhtmltopdf's CSS Handling

Odoo 18 uses **wkhtmltopdf** to convert HTML reports to PDF. wkhtmltopdf is notorious for:

- **Ignoring many CSS rules** that work in browsers
- **Not supporting CSS custom properties** (CSS variables)
- **Inconsistent handling of `table-layout: fixed`**
- **Ignoring percentage widths** in many scenarios
- **Ignoring `<colgroup>` and `<col>` elements**
- **Ignoring `nth-child` selectors** for width assignment

### 2. Odoo's Base Template Has No Width Definitions

The base `sale.report_saleorder_document` template defines the table without any column width specifications:

```xml
<table class="o_has_total_table table o_main_table table-borderless">
    <thead>
        <tr>
            <th name="th_description" class="text-start">Description</th>
            <th name="th_quantity" class="text-end">Quantity</th>
            <!-- ... more columns without widths ... -->
        </tr>
    </thead>
</table>
```

When you add more columns via XPath, wkhtmltopdf distributes all columns evenly.

### 3. Bootstrap & Odoo CSS Override Your Styles

The table has classes like `table`, `o_main_table`, `table-borderless` which load Bootstrap and Odoo's report CSS. These stylesheets have high specificity rules that override your custom CSS, especially in PDF rendering.

### 4. CSS Load Order in PDF vs HTML

For PDF generation, Odoo uses `minimal_layout` template which loads assets differently:
- `web.report_assets_pdf` (includes reset.css)
- `web.report_assets_common` (includes Bootstrap)

Your inline `<style>` tags may be overridden by these compiled assets.

---

## What Didn't Work

We tried many approaches that work in browsers but **failed in wkhtmltopdf**:

### 1. CSS Percentage Widths (FAILED)
```css
/* This works in HTML but NOT in PDF */
.o_main_table th:nth-child(1) { width: 6% !important; }
.o_main_table th:nth-child(2) { width: 30% !important; }
```

### 2. Colgroup with CSS (FAILED)
```xml
<!-- wkhtmltopdf ignores this -->
<colgroup>
    <col style="width: 6%"/>
    <col style="width: 30%"/>
</colgroup>
```

### 3. Width Attribute on Columns (FAILED)
```xml
<!-- Also ignored by wkhtmltopdf -->
<col width="6%"/>
<th width="200">Description</th>
```

### 4. Inline Styles on TH Only (FAILED)
```xml
<!-- Not enough - wkhtmltopdf needs more -->
<th style="width: 30%;">Description</th>
```

### 5. Fixed Pixel Widths in CSS (FAILED)
```css
/* Still ignored */
.o_main_table th:nth-child(2) { width: 200px !important; }
```

### 6. Hidden Sizing Row Technique (FAILED)
```xml
<!-- Common workaround that didn't work here -->
<tbody class="sizing-row">
    <tr style="height: 0;">
        <td style="width: 200px;"/>
    </tr>
</tbody>
```

### 7. XPath Replace on Individual Elements (FAILED)
Using XPath to replace `<thead>` and `<tbody>` separately while keeping the original `<table>` element preserved Odoo's CSS classes that override widths.

---

## The Solution

### The Key Insight

**You must replace the ENTIRE table element** with a custom one that:
1. Has **NO Odoo/Bootstrap CSS classes**
2. Uses **inline styles on EVERY element** (table, th, td)
3. Uses `table-layout: fixed` directly on the table
4. Includes `<colgroup>` as backup (some versions respect it)

### Why This Works

When you replace the entire table:
- You eliminate all inherited CSS classes (`table`, `o_main_table`, etc.)
- wkhtmltopdf has no external CSS rules to apply
- Inline styles become the ONLY source of styling
- `table-layout: fixed` is respected when there are no conflicting rules

### The Solution Code

```xml
<!-- Replace entire table with custom one that has inline styles -->
<xpath expr="//table[contains(@class, 'o_main_table')]" position="replace">
    <table class="o_ignore_layout_styling" border="0" cellpadding="0" cellspacing="0"
           style="width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 10px; border: none;">
        <colgroup>
            <col style="width: 6%"/>
            <col style="width: 30%"/>
            <col style="width: 20%"/>
            <col style="width: 9%"/>
            <col style="width: 8%"/>
            <col style="width: 9%"/>
            <col style="width: 5%"/>
            <col style="width: 6%"/>
            <col style="width: 7%"/>
        </colgroup>
        <thead>
            <tr>
                <th style="width: 6%; text-align: left; padding: 4px; font-size: 10px;">Internal Ref</th>
                <th style="width: 30%; text-align: left; padding: 4px; font-size: 10px;">Description</th>
                <th style="width: 20%; text-align: left; padding: 4px; font-size: 10px;">Lot/Serial Number</th>
                <th style="width: 9%; text-align: left; padding: 4px; font-size: 10px;">Expiration Date</th>
                <th style="width: 8%; text-align: right; padding: 4px; font-size: 10px;">Quantity</th>
                <th style="width: 9%; text-align: right; padding: 4px; font-size: 10px;">Unit Price</th>
                <th style="width: 5%; text-align: right; padding: 4px; font-size: 10px;">Disc.%</th>
                <th style="width: 6%; text-align: right; padding: 4px; font-size: 10px;">Taxes</th>
                <th style="width: 7%; text-align: right; padding: 4px; font-size: 10px;">Amount</th>
            </tr>
        </thead>
        <tbody>
            <t t-set="lines_to_report" t-value="doc._get_order_lines_to_report()"/>
            <t t-foreach="lines_to_report" t-as="line">
                <tr t-if="not line.display_type">
                    <td style="width: 6%; padding: 4px; font-size: 10px;"><span t-field="line.product_id.default_code"/></td>
                    <td style="width: 30%; padding: 4px; font-size: 10px;"><span t-field="line.name"/></td>
                    <td style="width: 20%; padding: 4px; font-size: 10px;"><span t-field="line.lot_id"/></td>
                    <td style="width: 9%; padding: 4px; font-size: 10px;">
                        <t t-if="line.lot_expiration_date">
                            <span t-out="line.lot_expiration_date.date().strftime('%d-%m-%Y')"/>
                        </t>
                    </td>
                    <td style="width: 8%; text-align: right; padding: 4px; font-size: 10px;">
                        <span t-field="line.product_uom_qty"/> <span t-field="line.product_uom"/>
                    </td>
                    <td style="width: 9%; text-align: right; padding: 4px; font-size: 10px;">
                        <span t-field="line.price_unit"/>
                    </td>
                    <td style="width: 5%; text-align: right; padding: 4px; font-size: 10px;">
                        <span t-field="line.discount"/>
                    </td>
                    <td style="width: 6%; text-align: right; padding: 4px; font-size: 10px;">
                        <span t-field="line.tax_id"/>
                    </td>
                    <td style="width: 7%; text-align: right; padding: 4px; font-size: 10px;">
                        <span t-field="line.price_subtotal"
                              t-options='{"widget": "monetary", "display_currency": doc.currency_id}'/>
                    </td>
                </tr>
                <tr t-if="line.display_type == 'line_section'">
                    <td colspan="9" style="padding: 4px; font-weight: bold; font-size: 10px;">
                        <span t-field="line.name"/>
                    </td>
                </tr>
                <tr t-if="line.display_type == 'line_note'">
                    <td colspan="9" style="padding: 4px; font-style: italic; font-size: 10px;">
                        <span t-field="line.name"/>
                    </td>
                </tr>
            </t>
        </tbody>
    </table>
</xpath>
```

### Critical Elements

| Element | Purpose |
|---------|---------|
| `class="o_ignore_layout_styling"` | Excludes table from Odoo's automatic styling |
| `border="0" cellpadding="0" cellspacing="0"` | HTML attributes as backup |
| `style="table-layout: fixed;"` | Forces browser to respect column widths |
| `style="width: X%"` on every th/td | Inline styles that wkhtmltopdf can't ignore |
| `font-size: 10px` | Smaller text prevents overflow |

---

## Removing Unwanted Borders

After replacing the table, you may see unwanted borders from Odoo's report layout CSS (especially with boxed layouts). These come from `::before` and `::after` pseudo-elements.

### Add This CSS to Your Style Block

```css
/* Remove outer box/border from main table only - target pseudo-elements */
.page table.o_ignore_layout_styling,
.page table.o_ignore_layout_styling::before,
.page table.o_ignore_layout_styling::after,
.article table.o_ignore_layout_styling,
.article table.o_ignore_layout_styling::before,
.article table.o_ignore_layout_styling::after {
    border: none !important;
    border-width: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    border-radius: 0 !important;
    content: none !important;
}
```

### Important Notes

- Target `::before` and `::after` pseudo-elements (Odoo uses these for boxed borders)
- Use `content: none !important` to completely remove pseudo-elements
- Scope to `.o_ignore_layout_styling` so you don't affect the totals table

---

## Complete Working Example

Here's the complete XML file structure:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_saleorder_document" inherit_id="sale.report_saleorder_document" priority="100">

        <!-- Add style block inside external_layout -->
        <xpath expr="//t[@t-call='web.external_layout']" position="inside">
            <style type="text/css">
                /* Remove outer box/border from main table only */
                .page table.o_ignore_layout_styling,
                .page table.o_ignore_layout_styling::before,
                .page table.o_ignore_layout_styling::after,
                .article table.o_ignore_layout_styling,
                .article table.o_ignore_layout_styling::before,
                .article table.o_ignore_layout_styling::after {
                    border: none !important;
                    border-width: 0 !important;
                    box-shadow: none !important;
                    outline: none !important;
                    border-radius: 0 !important;
                    content: none !important;
                }
            </style>
        </xpath>

        <!-- Replace entire table -->
        <xpath expr="//table[contains(@class, 'o_main_table')]" position="replace">
            <table class="o_ignore_layout_styling" border="0" cellpadding="0" cellspacing="0"
                   style="width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 10px; border: none; box-shadow: none; outline: none; border-radius: 0;">
                <colgroup>
                    <col style="width: 6%"/>
                    <col style="width: 30%"/>
                    <col style="width: 20%"/>
                    <!-- ... more columns ... -->
                </colgroup>
                <thead>
                    <tr>
                        <th style="width: 6%; text-align: left; padding: 4px; font-size: 10px;">Internal Ref</th>
                        <th style="width: 30%; text-align: left; padding: 4px; font-size: 10px;">Description</th>
                        <!-- ... more headers with inline styles ... -->
                    </tr>
                </thead>
                <tbody>
                    <t t-set="lines_to_report" t-value="doc._get_order_lines_to_report()"/>
                    <t t-foreach="lines_to_report" t-as="line">
                        <tr t-if="not line.display_type">
                            <td style="width: 6%; padding: 4px; font-size: 10px;">
                                <span t-field="line.product_id.default_code"/>
                            </td>
                            <!-- ... more cells with inline styles ... -->
                        </tr>
                    </t>
                </tbody>
            </table>
        </xpath>

    </template>
</odoo>
```

---

## Tips & Best Practices

### 1. Always Test Both HTML and PDF
```
HTML: /report/html/sale.report_saleorder/123
PDF:  /report/pdf/sale.report_saleorder/123
```

### 2. Column Width Percentages Must Add to 100%
```
6% + 30% + 20% + 9% + 8% + 9% + 5% + 6% + 7% = 100%
```

### 3. Use Smaller Font Size for Many Columns
With 9 columns, use `font-size: 10px` or smaller to prevent text overflow.

### 4. Add `word-wrap: break-word` for Long Content
```xml
<td style="width: 30%; padding: 4px; font-size: 10px; word-wrap: break-word;">
```

### 5. Handle Section and Note Lines
Don't forget to handle `line.display_type == 'line_section'` and `'line_note'` with `colspan`.

### 6. Don't Forget to Upgrade the Module
```bash
./odoo-bin -c <config> -d <database> -u <module_name> --stop-after-init
```

### 7. Clear Browser Cache
After changes, clear browser cache or use incognito mode to see updates.

### 8. Check wkhtmltopdf Version
```bash
wkhtmltopdf --version
```
Odoo 18 requires wkhtmltopdf 0.12.5 or later with patched Qt.

---

## Troubleshooting

### PDF shows equal columns despite changes
- Ensure you're replacing the ENTIRE table, not just modifying it
- Check that no Odoo CSS classes remain on the table
- Verify inline styles are on EVERY th and td element

### Borders appear around table in PDF
- Add `o_ignore_layout_styling` class to table
- Target `::before` and `::after` pseudo-elements in CSS
- Use `content: none !important`

### Text overflows columns
- Reduce `font-size` (try 9px or 10px)
- Add `word-wrap: break-word`
- Adjust column width percentages

### Changes not appearing
- Upgrade the module
- Clear browser cache
- Restart Odoo server
- Check for XML syntax errors in logs

### Totals table lost its border
- Make CSS selectors specific to `.o_ignore_layout_styling`
- Don't use broad selectors like `.page table`

---

## Summary

| Approach | HTML | PDF | Verdict |
|----------|------|-----|---------|
| CSS nth-child selectors | ✅ | ❌ | Don't use |
| Colgroup with CSS | ✅ | ❌ | Don't use |
| XPath modify existing table | ✅ | ❌ | Don't use |
| **Replace entire table + inline styles** | ✅ | ✅ | **USE THIS** |

### The Golden Rule

> **For wkhtmltopdf compatibility, replace the entire table element and use inline styles on every single element. Remove all Odoo/Bootstrap CSS classes.**

---

**Last Updated:** January 2026
**Tested on:** Odoo 18.0
**wkhtmltopdf:** 0.12.6 (with patched Qt)
