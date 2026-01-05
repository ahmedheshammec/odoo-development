# Partner Sign Block (Sale Order Report)

This doc shows full, copy‑pasteable QWeb snippets for adding signature blocks to the Sale Order PDF report. It includes:
- 9 signatures (3×3) — current layout
- 10 signatures (5×2) — example
- 8 signatures (4×2) — example
- Safe version that never errors if total isn’t divisible by columns

Path used in this project:
`/Volumes/Samsung T5/Odoo/Odoo/Ha & HO/hassan_live_2_1_2026/so_print/views/report_saleorder.xml`

---

## Base block (table + styling)
Use this wrapper and only replace the inner loops + labels in each example.

```xml
<div class="mt32 so-print-signatures-wrap">
    <style>
        .so-print-signatures-wrap,
        .so-print-signatures-wrap * {
            box-shadow: none !important;
        }
        .so-print-signatures-wrap,
        .so-print-signatures,
        .so-print-signatures tbody,
        .so-print-signatures tr,
        .so-print-signatures td {
            border: 0 !important;
            outline: 0 !important;
            background: transparent !important;
        }
    </style>

    <!-- REPLACE THIS WITH ONE OF THE EXAMPLES BELOW -->
</div>
```

Signature cell template (used in all examples):

```xml
<td style="width: 33.33%; text-align: center; vertical-align: top; padding: 0; border: 0 !important;">
    <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
        <t t-esc="sign_labels[i]"/>
    </h1>
    <div style="height: 28px;"></div>
    <div style="border-bottom: 1px dashed #000; width: 80%; margin: 0 auto; border-left: 0; border-right: 0; border-top: 0;"></div>
</td>
```

---

## Example 1: 9 signatures (3×3)

```xml
<t t-set="sign_labels"
   t-value="['الطرف الأول', 'الطرف الثاني', 'الطرف الثالث', 'الطرف الرابع', 'الطرف الخامس', 'الطرف السادس', 'الطرف السابع', 'الطرف الثامن', 'الطرف التاسع']"/>

<table class="so-print-signatures" border="0" cellpadding="0" cellspacing="0"
       style="width: 100%; border-collapse: collapse; border: 0 !important; border-style: none; border-color: transparent !important; border-spacing: 0; margin: 0; padding: 0; outline: 0 !important; background: transparent !important;">
    <t t-foreach="range(0, 9, 3)" t-as="row_start">
        <tr style="border: 0 !important;">
            <t t-foreach="range(row_start, row_start + 3)" t-as="i">
                <td style="width: 33.33%; text-align: center; vertical-align: top; padding: 0; border: 0 !important;">
                    <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
                        <t t-esc="sign_labels[i]"/>
                    </h1>
                    <div style="height: 28px;"></div>
                    <div style="border-bottom: 1px dashed #000; width: 80%; margin: 0 auto; border-left: 0; border-right: 0; border-top: 0;"></div>
                </td>
            </t>
        </tr>
        <tr t-if="row_start != 6">
            <td colspan="3" style="height: 60px; padding: 0; border: 0 !important;"></td>
        </tr>
    </t>
</table>
```

---

## Example 2: 10 signatures (5×2)

```xml
<t t-set="sign_labels"
   t-value="['الطرف 1', 'الطرف 2', 'الطرف 3', 'الطرف 4', 'الطرف 5', 'الطرف 6', 'الطرف 7', 'الطرف 8', 'الطرف 9', 'الطرف 10']"/>

<table class="so-print-signatures" border="0" cellpadding="0" cellspacing="0"
       style="width: 100%; border-collapse: collapse; border: 0 !important; border-style: none; border-color: transparent !important; border-spacing: 0; margin: 0; padding: 0; outline: 0 !important; background: transparent !important;">
    <t t-foreach="range(0, 10, 2)" t-as="row_start">
        <tr style="border: 0 !important;">
            <t t-foreach="range(row_start, row_start + 2)" t-as="i">
                <td style="width: 50%; text-align: center; vertical-align: top; padding: 0; border: 0 !important;">
                    <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
                        <t t-esc="sign_labels[i]"/>
                    </h1>
                    <div style="height: 28px;"></div>
                    <div style="border-bottom: 1px dashed #000; width: 80%; margin: 0 auto; border-left: 0; border-right: 0; border-top: 0;"></div>
                </td>
            </t>
        </tr>
        <tr t-if="row_start != 8">
            <td colspan="2" style="height: 60px; padding: 0; border: 0 !important;"></td>
        </tr>
    </t>
</table>
```

---

## Example 3: 8 signatures (4×2)

```xml
<t t-set="sign_labels"
   t-value="['الطرف 1', 'الطرف 2', 'الطرف 3', 'الطرف 4', 'الطرف 5', 'الطرف 6', 'الطرف 7', 'الطرف 8']"/>

<table class="so-print-signatures" border="0" cellpadding="0" cellspacing="0"
       style="width: 100%; border-collapse: collapse; border: 0 !important; border-style: none; border-color: transparent !important; border-spacing: 0; margin: 0; padding: 0; outline: 0 !important; background: transparent !important;">
    <t t-foreach="range(0, 8, 2)" t-as="row_start">
        <tr style="border: 0 !important;">
            <t t-foreach="range(row_start, row_start + 2)" t-as="i">
                <td style="width: 50%; text-align: center; vertical-align: top; padding: 0; border: 0 !important;">
                    <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
                        <t t-esc="sign_labels[i]"/>
                    </h1>
                    <div style="height: 28px;"></div>
                    <div style="border-bottom: 1px dashed #000; width: 80%; margin: 0 auto; border-left: 0; border-right: 0; border-top: 0;"></div>
                </td>
            </t>
        </tr>
        <tr t-if="row_start != 6">
            <td colspan="2" style="height: 60px; padding: 0; border: 0 !important;"></td>
        </tr>
    </t>
</table>
```

---

## Safe version (never errors if total isn’t divisible by columns)
This version guards the index, so you can use any total with any column count.

```xml
<t t-set="sign_labels"
   t-value="['الطرف 1', 'الطرف 2', 'الطرف 3', 'الطرف 4', 'الطرف 5', 'الطرف 6', 'الطرف 7', 'الطرف 8', 'الطرف 9', 'الطرف 10']"/>
<t t-set="total" t-value="len(sign_labels)"/>
<t t-set="cols" t-value="3"/>

<table class="so-print-signatures" border="0" cellpadding="0" cellspacing="0"
       style="width: 100%; border-collapse: collapse; border: 0 !important; border-style: none; border-color: transparent !important; border-spacing: 0; margin: 0; padding: 0; outline: 0 !important; background: transparent !important;">
    <t t-foreach="range(0, total, cols)" t-as="row_start">
        <tr style="border: 0 !important;">
            <t t-foreach="range(row_start, row_start + cols)" t-as="i">
                <t t-if="i &lt; total">
                    <td style="width: calc(100% / 3); text-align: center; vertical-align: top; padding: 0; border: 0 !important;">
                        <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
                            <t t-esc="sign_labels[i]"/>
                        </h1>
                        <div style="height: 28px;"></div>
                        <div style="border-bottom: 1px dashed #000; width: 80%; margin: 0 auto; border-left: 0; border-right: 0; border-top: 0;"></div>
                    </td>
                </t>
                <t t-else="">
                    <td style="width: calc(100% / 3); padding: 0; border: 0 !important;"></td>
                </t>
            </t>
        </tr>
        <tr t-if="row_start + cols &lt; total">
            <td colspan="3" style="height: 60px; padding: 0; border: 0 !important;"></td>
        </tr>
    </t>
</table>
```

Notes for safe version:
- Change `cols` to the number of columns you want.
- Update the `width: calc(100% / 3)` and `colspan="3"` to match the same column count.
- Use `total = len(sign_labels)` to auto-size based on labels.

