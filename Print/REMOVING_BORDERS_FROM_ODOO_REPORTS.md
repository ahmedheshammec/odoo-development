# How to Remove Borders from Odoo Report Tables

This guide explains how to completely remove borders from custom table elements in Odoo 18 reports while keeping specific styling like dashed lines.

## The Problem

When adding custom tables to Odoo reports, they automatically inherit border styling from Odoo's report CSS. These borders come from:

1. **Odoo's table styling classes** in `/addons/web/static/src/webclient/actions/reports/report_tables.scss`
2. **Pseudo-elements (`::before`, `::after`)** used by boxed table layouts
3. **Parent container styling** from the report layout

Even with inline styles like `border: none !important;`, borders may still appear because Odoo's CSS rules have high specificity.

## The Solution

### Step 1: Use the `o_ignore_layout_styling` Class

Odoo provides a special class that excludes tables from automatic styling:

```xml
<table class="o_ignore_layout_styling" border="0" cellpadding="0" cellspacing="0">
    <!-- your table content -->
</table>
```

All Odoo's table styling rules use `table:not(.o_ignore_layout_styling)`, so adding this class prevents automatic borders.

### Step 2: Add a Container with Custom CSS

Wrap your table in a container div with aggressive CSS that targets pseudo-elements:

```xml
<style>
    /* Completely remove borders from signature section */
    .your-custom-container,
    .your-custom-container::before,
    .your-custom-container::after,
    .your-custom-container table,
    .your-custom-container table::before,
    .your-custom-container table::after,
    .your-custom-container tbody,
    .your-custom-container tbody::before,
    .your-custom-container tbody::after,
    .your-custom-container tr,
    .your-custom-container tr::before,
    .your-custom-container tr::after,
    .your-custom-container td,
    .your-custom-container td::before,
    .your-custom-container td::after {
        border: none !important;
        border-width: 0 !important;
        border-style: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Keep specific borders like dashed lines */
    .your-custom-container .signature-line {
        border-bottom: 1px dashed #000 !important;
    }
</style>

<div class="your-custom-container" style="margin-top: 32px; border: none !important;">
    <table class="o_ignore_layout_styling" border="0" cellpadding="0" cellspacing="0"
           style="width: 100% !important; border: none !important; border-collapse: collapse !important;">
        <!-- your table content -->
    </table>
</div>
```

### Step 3: Add Inline Styles as Backup

Even with the CSS above, add inline styles to every table element:

```xml
<table class="o_ignore_layout_styling" border="0" cellpadding="0" cellspacing="0"
       style="width: 100% !important; border: none !important; border-width: 0px !important;
              border-style: none !important; border-collapse: collapse !important;
              margin: 0 !important; padding: 0 !important;">
    <tr style="border: none !important; border-width: 0px !important;">
        <td style="border: none !important; border-width: 0px !important; border-style: none !important;
                   padding: 0 !important; margin: 0 !important;">
            <!-- cell content -->
        </td>
    </tr>
</table>
```

## Complete Working Example

Here's a complete example that removes all borders while keeping dashed signature lines:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_saleorder_document_inherit_signatures" inherit_id="sale.report_saleorder_document">
        <xpath expr="//div[contains(@class, 'page')]" position="inside">
            <style>
                /* Completely remove borders from signature section */
                .so-print-signatures-container,
                .so-print-signatures-container::before,
                .so-print-signatures-container::after,
                .so-print-signatures-container table,
                .so-print-signatures-container table::before,
                .so-print-signatures-container table::after,
                .so-print-signatures-container tbody,
                .so-print-signatures-container tbody::before,
                .so-print-signatures-container tbody::after,
                .so-print-signatures-container tr,
                .so-print-signatures-container tr::before,
                .so-print-signatures-container tr::after,
                .so-print-signatures-container td,
                .so-print-signatures-container td::before,
                .so-print-signatures-container td::after {
                    border: none !important;
                    border-width: 0 !important;
                    border-style: none !important;
                    outline: none !important;
                    box-shadow: none !important;
                }
                /* Keep the dashed signature lines */
                .so-print-signatures-container .signature-line {
                    border-bottom: 1px dashed #000 !important;
                }
            </style>

            <div class="so-print-signatures-container" style="margin-top: 32px; border: none !important;">
                <t t-set="sign_labels"
                   t-value="['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5', 'Label 6']"/>

                <table class="o_ignore_layout_styling" border="0" cellpadding="0" cellspacing="0"
                       style="width: 100% !important; border: none !important; border-width: 0px !important;
                              border-style: none !important; border-collapse: collapse !important;
                              margin: 0 !important; padding: 0 !important;">
                    <t t-foreach="range(0, 6, 3)" t-as="row_start">
                        <tr style="border: none !important; border-width: 0px !important;">
                            <t t-foreach="range(row_start, min(row_start + 3, 6))" t-as="i">
                                <td style="width: 33.33% !important; text-align: center !important;
                                           vertical-align: top !important; padding: 0 !important;
                                           margin: 0 !important; border: none !important;
                                           border-width: 0px !important; border-style: none !important;">
                                    <h1 style="font-size: 20px; font-weight: 900; text-align: center; margin: 0;">
                                        <t t-esc="sign_labels[i]"/>
                                    </h1>
                                    <div style="height: 28px;"></div>
                                    <div class="signature-line"
                                         style="border-bottom: 1px dashed #000; width: 80%; margin: 0 auto;
                                                border-left: none; border-right: none; border-top: none;"></div>
                                </td>
                            </t>
                            <!-- Fill empty cells to maintain grid -->
                            <t t-foreach="range(min(row_start + 3, 6) - row_start, 3)" t-as="empty">
                                <td style="width: 33.33% !important; padding: 0 !important;
                                           border: none !important; border-width: 0px !important;
                                           border-style: none !important;"></td>
                            </t>
                        </tr>
                        <tr t-if="row_start != 3" style="border: none !important; border-width: 0px !important;">
                            <td colspan="3" style="height: 60px; padding: 0 !important;
                                                   border: none !important; border-width: 0px !important;
                                                   border-style: none !important;"></td>
                        </tr>
                    </t>
                </table>
            </div>
        </xpath>
    </template>
</odoo>
```

## Key Points

1. **`o_ignore_layout_styling` class** - Essential for excluding from Odoo's automatic table styling
2. **Target pseudo-elements** - `::before` and `::after` are critical as Odoo's boxed layouts use them for borders
3. **Container CSS** - Wrap in a container with specific class to scope your CSS rules
4. **Inline styles** - Add as backup for maximum compatibility
5. **Preserve specific borders** - Use a class like `.signature-line` to keep dashed lines or other desired borders

## Odoo's Table Styling Source

The borders come from these selectors in `/addons/web/static/src/webclient/actions/reports/report_tables.scss`:

- `.o_table_standard table:not(.o_ignore_layout_styling)`
- `.o_table_boxed table:not(.o_ignore_layout_styling)::before`
- `.o_table_striped table:not(.o_ignore_layout_styling)`

By using `o_ignore_layout_styling`, you opt out of all these automatic stylings.

## Troubleshooting

If borders still appear after following these steps:

1. **Clear browser cache** and regenerate the PDF
2. **Update the module** to ensure CSS changes are loaded
3. **Check for conflicting CSS** in other modules
4. **Inspect the PDF** to identify which CSS rule is applying the border
5. **Add more specific selectors** to your CSS to override stubborn rules

---

**Last Updated:** January 2026
**Tested on:** Odoo 18.0
