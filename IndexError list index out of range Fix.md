# Custom Invoice Report Error Fixes (Odoo 19)

This document records the fixes applied to resolve the repetitive PDF print errors while building the `custom_invoice` report.

## Error 1: `IndexError: list index out of range` (missing `<main>`)
**Symptom**
```
IndexError: list index out of range
... ir_actions_report.py ... _prepare_html
body_parent = root.xpath('//main')[0]
```

**Cause**
The final report HTML did not contain a `<main>` element. Odoo’s report renderer expects a `<main>` tag in the output generated via `web.html_container`/`web.external_layout`.

**Fix**
Wrap the report content inside `web.html_container` and `web.external_layout`, and add a `<main>` element so the renderer always finds it.

**Snippet (final structure)**
```xml
<template id="report_custom_invoice_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="web.external_layout">
                <main>
                    <div class="page">
                        <!-- report content -->
                    </div>
                </main>
            </t>
        </t>
    </t>
</template>
```

## Error 2: `ValueError: Fetching report ... expected ir.actions.report`
**Symptom**
```
ValueError: Fetching report 'custom_invoice.report_custom_invoice_document':
 type ir.ui.view, expected ir.actions.report
```

**Cause**
The report action (`ir.actions.report`) pointed to a template name that was being resolved as an `ir.ui.view` instead of the action’s `report_name`. Odoo resolves the report by name via `ir.actions.report` and fails if it finds a view instead.

**Fix**
Make the `report_name` and `report_file` match the actual report template ID being rendered.

**Snippet (action definition)**
```xml
<record id="action_report_custom_invoice" model="ir.actions.report">
    <field name="name">Custom Invoice</field>
    <field name="model">account.move</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">custom_invoice.report_custom_invoice_document</field>
    <field name="report_file">custom_invoice.report_custom_invoice_document</field>
    <field name="binding_model_id" ref="account.model_account_move"/>
    <field name="binding_type">report</field>
    <field name="print_report_name">'Custom Invoice - %s' % (object.name)</field>
</record>
```

## Final Notes
- Always ensure the report template renders through `web.html_container` and includes a `<main>` tag.
- Make sure `report_name`/`report_file` match a valid `ir.actions.report` and not just a template ID.
- After changes: restart Odoo and upgrade the module.

**Files touched**
- `custom_invoice/report/custom_invoice_report.xml`
