# Print Implementation Guide (Calibri / Minimal Template)

This folder contains a working print setup (copied from `property` module):
- `property_delegation_report.xml` – QWeb template + paperformat + ir.actions.report
- `font_calibri_alfont.css` – embedded Calibri base64 font
- `property_delegation_report.css` – layout styles (matches legal_affairs_dep)

Use these snippets to add the same baseline print to another module.

## 1) Manifest
```python
'assets': {
    'web.report_assets_common': [
        'your_module/static/src/css/font_calibri_alfont.css',
        'your_module/static/src/css/<your_report>.css',
    ],
},
'data': [
    'report/<your_report>.xml',
],
```

## 2) Paperformat + Report Action (QWeb PDF in Settings cog)
```xml
<record id="paperformat_X" model="report.paperformat">
    <field name="name">X</field>
    <field name="format">A4</field>
    <field name="page_height">0</field>
    <field name="page_width">0</field>
    <field name="orientation">Portrait</field>
    <field name="margin_top">60</field>
    <field name="margin_bottom">20</field>
    <field name="margin_left">0</field>
    <field name="margin_right">0</field>
    <field name="header_line" eval="False"/>
    <field name="header_spacing">0</field>
    <field name="dpi">90</field>
</record>

<record id="action_report_X" model="ir.actions.report">
    <field name="name">X</field>
    <field name="model">your.model</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">your_module.report_X_document</field>
    <field name="report_file">your_module.report_X_document</field>
    <field name="binding_model_id" ref="model_your_model"/>
    <field name="binding_type">report</field>
    <field name="print_report_name">'X - %s' % (object.display_name or 'X')</field>
    <field name="paperformat_id" ref="paperformat_X"/>
</record>
```

## 3) Template Skeleton (uses Calibri + included CSS)
```xml
<template id="report_X_document">
  <t t-call="web.html_container">
    <meta charset="UTF-8"/>
    <t t-call-assets="web.report_assets_common" t-js="false"/>
    <t t-foreach="docs" t-as="o">
      <div class="page" style="page-break-after: always; position: relative;">
        <div class="oe_structure"/>
        <div class="content-wrapper">
          <!-- Header block (Arabic text, dates, parties) -->
          <!-- Copy/adapt from property_delegation_report.xml -->
          <!-- Example fields: o.date, o.hijri_date, company fields, partner fields -->

          <!-- Signature block -->
          <table style="width:100%; border-collapse: collapse; border: 0 !important;">
            <tr>
              <td style="width:25%; text-align:left; vertical-align:top; padding:0; border:0 !important;">
                <h1>... الطرف الثاني ...</h1>
                <span t-field="o.customer_id.display_name"/>
              </td>
              <td style="width:50%; border:0 !important;"></td>
              <td style="width:25%; text-align:right; vertical-align:top; padding:0; border:0 !important;">
                <h1>... الطرف الأول ...</h1>
                <span t-field="company.name"/>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </t>
  </t>
</template>
```

## 4) CSS
- Copy `font_calibri_alfont.css` as-is (embedded Calibri Regular/Bold).
- Create `<your_report>.css` by reusing `property_delegation_report.css` (layout, typography, table rules, and helper classes).

## 5) Files to copy as a starting point
From this folder to your module:
- `font_calibri_alfont.css`  -> `your_module/static/src/css/`
- `property_delegation_report.css` -> rename if desired -> `your_module/static/src/css/`
- `property_delegation_report.xml` -> adapt IDs/names/model/fields -> `your_module/report/`

## 6) Model binding
Ensure `binding_model_id` uses the target model (e.g., `model_property_delegation`). The action automatically shows under the cog/print menu for that model.

## 7) Upgrade
After copying & adjusting, update the module (e.g., `-u your_module`) so assets and report are registered.
