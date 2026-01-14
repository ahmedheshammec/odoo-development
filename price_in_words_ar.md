# Arabic Price In Words (Odoo)

This document explains how the `price_in_words_ar` logic works, where it is defined, and how to reuse it in future Odoo modules and reports.

## Where it lives

- Report usage: `print_papers/reports/agreement_report.xml` renders the Arabic words in the agreement QWeb report.
- Logic: `property/models/models.py` defines a computed field `price_in_words_ar` and a helper method `_number_to_arabic_words`.

## Requirements

- No external Python libraries are required.
- The logic relies only on standard Odoo model methods and standard Python.

## How the current implementation works

### 1) Computed field on the model

The field is computed from `price` and is not stored in the database. When `price` changes, the computed field recalculates automatically.

```python
price_in_words_ar = fields.Char(
    string="Price in Arabic Words",
    compute="_compute_price_in_words",
    store=False
)

@api.depends('price')
def _compute_price_in_words(self):
    for record in self:
        if record.price:
            record.price_in_words_ar = self._number_to_arabic_words(record.price)
        else:
            record.price_in_words_ar = ''
```

Explanation:
- `@api.depends('price')` ensures the computation runs whenever `price` changes.
- If `price` is zero or empty, it returns an empty string (you can change this to `صفر` if you prefer).
- The actual conversion is delegated to `_number_to_arabic_words`.

### 2) Number-to-words conversion logic

The helper breaks a number into billions, millions, thousands, and the remaining part below 1000.
It then joins the Arabic phrases with the conjunction `و` ("and") to form the final result.

```python
def _number_to_arabic_words(self, number):
    """Convert number to Arabic words"""
    if number == 0:
        return "صفر"

    ones = ['', 'واحد', 'اثنان', 'ثلاثة', 'أربعة', 'خمسة', 'ستة', 'سبعة', 'ثمانية', 'تسعة']
    tens = ['', 'عشرة', 'عشرون', 'ثلاثون', 'أربعون', 'خمسون', 'ستون', 'سبعون', 'ثمانون', 'تسعون']
    hundreds = ['', 'مائة', 'مائتان', 'ثلاثمائة', 'أربعمائة', 'خمسمائة', 'ستمائة', 'سبعمائة', 'ثماني مائة',
                'تسعمائة']
    teens = ['عشرة', 'أحد عشر', 'اثنا عشر', 'ثلاثة عشر', 'أربعة عشر', 'خمسة عشر', 'ستة عشر', 'سبعة عشر',
             'ثمانية عشر', 'تسعة عشر']

    def convert_below_thousand(num):
        if num == 0:
            return ''
        elif num < 10:
            return ones[num]
        elif num < 20:
            return teens[num - 10]
        elif num < 100:
            return tens[num // 10] + (' و' + ones[num % 10] if num % 10 != 0 else '')
        else:
            return hundreds[num // 100] + (' و' + convert_below_thousand(num % 100) if num % 100 != 0 else '')

    num = int(number)
    if num == 0:
        return "صفر"

    result = []

    # Billions
    if num >= 1000000000:
        billions = num // 1000000000
        if billions == 1:
            result.append('مليار')
        elif billions == 2:
            result.append('ملياران')
        elif billions <= 10:
            result.append(convert_below_thousand(billions) + ' مليار')
        else:
            result.append(convert_below_thousand(billions) + ' مليار')
        num = num % 1000000000

    # Millions
    if num >= 1000000:
        millions = num // 1000000
        if millions == 1:
            result.append('مليون')
        elif millions == 2:
            result.append('مليونان')
        elif millions <= 10:
            result.append(convert_below_thousand(millions) + ' ملايين')
        else:
            result.append(convert_below_thousand(millions) + ' مليون')
        num = num % 1000000

    # Thousands
    if num >= 1000:
        thousands = num // 1000
        if thousands == 1:
            result.append('ألف')
        elif thousands == 2:
            result.append('ألفان')
        elif thousands <= 10:
            result.append(convert_below_thousand(thousands) + ' آلاف')
        else:
            result.append(convert_below_thousand(thousands) + ' ألف')
        num = num % 1000

    # Remaining
    if num > 0:
        result.append(convert_below_thousand(num))

    return ' و'.join(result)
```

Key points:
- The algorithm always reduces the number from largest group to smallest.
- It uses `convert_below_thousand` to format a chunk between 1 and 999.
- Arabic grammatical variants are handled for 1, 2, and 3–10 in thousands/millions/billions.
- The final phrase is concatenated with `و` as a natural Arabic joiner.

Example:
- `700` becomes `سبعمائة` (via `convert_below_thousand`).
- `1,200` becomes `ألف و مائتان`.
- `2,000,000` becomes `مليونان`.

## Where it is used in the report

In `print_papers/reports/agreement_report.xml` the field is displayed as:

```xml
<span t-field="o.apartment_number_id.price_in_words_ar"/> ريال
```

This means the QWeb report prints the Arabic words next to the currency label.

## How to reuse in future projects

### A) Reuse in another model

1) Add the computed field to your model:

```python
price_in_words_ar = fields.Char(
    string="Price in Arabic Words",
    compute="_compute_price_in_words",
    store=False
)
```

2) Add the compute method and helper (you can copy exactly from `property/models/models.py`).

3) Ensure your model has a numeric `price` (or any amount field you want to convert).

If your field is named differently (for example `amount_total`), update the dependency:

```python
@api.depends('amount_total')
def _compute_price_in_words(self):
    for record in self:
        record.price_in_words_ar = self._number_to_arabic_words(record.amount_total or 0)
```

### B) Reuse in a report

Once the field exists, add it in your QWeb template:

```xml
<span t-field="o.price_in_words_ar"/> ريال
```

If the field is on a related record (as in the agreement report), reference it with dot notation:

```xml
<span t-field="o.apartment_number_id.price_in_words_ar"/> ريال
```

### C) Optional: make it a reusable mixin

If multiple models need the same functionality, you can move the helper and compute logic to a mixin model, then inherit it from your business models.

Example pattern:

```python
class ArabicWordsMixin(models.AbstractModel):
    _name = "arabic.words.mixin"

    def _number_to_arabic_words(self, number):
        # (same helper code)
        pass
```

Then inherit it where needed:

```python
class SomeModel(models.Model):
    _name = "some.model"
    _inherit = ["arabic.words.mixin"]
```

## Notes and limitations

- The logic casts to `int`, so decimal fractions are dropped. If you need cents/halalas, you will need to extend the function.
- The current output uses the masculine form where applicable and focuses on general numeric wording for currency totals.

## Quick checklist for future use

- Ensure `price_in_words_ar` is computed and available on the model used in your report.
- Confirm the report template uses `t-field` to render the computed value.
- No external libraries or pip installs are required.
