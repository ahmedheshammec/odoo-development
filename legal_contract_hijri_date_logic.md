# Hijri date + Arabic weekday logic (Odoo 18 legal_contract)

This document captures the Hijri conversion and Arabic weekday logic implemented in the Legal Affairs module, and shows how to reuse it in other Odoo projects.

## Where the logic lives

- Model: `models/legal_contract.py`
- Report usage: `report/legal_contract_report.xml`

## Dependency: hijridate library

The code uses the `hijridate` package (PyPI name: `hijridate`) and imports `Gregorian` from it.

### Install (system / venv)

```bash
pip install hijridate
```

### In Odoo deployments

- Add `hijridate` to your Python environment for the Odoo service.
- If you keep a requirements file for your deployment, add:

```
hijridate
```

### Import pattern used in the module

```python
try:
    from hijridate import Gregorian
except ImportError:
    Gregorian = None
```

This is a safe import. If the library is missing, `Gregorian` is set to `None` and Hijri values are left empty rather than crashing.

## Computed fields and how they work

The model computes two groups of fields from `start_date`:

- **Arabic weekday**
  - `start_date_day_name` (for report)
  - `arabic_day` (another exposed field)
- **Hijri date**
  - `start_date_hijri` (for report)
  - `hijri_date` (another exposed field)

All four fields are computed by the same method, and stored in the database.

### Field definitions (key parts)

```python
start_date = fields.Date(string='Start Date', required=True)

hijri_date = fields.Char(
    string='Hijri Date',
    compute='_compute_date_fields',
    store=True
)

arabic_day = fields.Char(
    string='Arabic Day',
    compute='_compute_date_fields',
    store=True
)

start_date_hijri = fields.Char(
    string='Start Date (Hijri)',
    compute='_compute_date_fields',
    store=True
)

start_date_day_name = fields.Char(
    string='Day of Week',
    compute='_compute_date_fields',
    store=True
)
```

### Compute method (full snippet)

```python
@api.depends('start_date')
def _compute_date_fields(self):
    """Compute Hijri date and day of week in Arabic"""
    arabic_days = {
        0: 'الاثنين',
        1: 'الثلاثاء',
        2: 'الأربعاء',
        3: 'الخميس',
        4: 'الجمعة',
        5: 'السبت',
        6: 'الأحد',
    }
    hijri_months = {
        1: 'محرم',
        2: 'صفر',
        3: 'ربيع الأول',
        4: 'ربيع الثاني',
        5: 'جمادى الأولى',
        6: 'جمادى الآخرة',
        7: 'رجب',
        8: 'شعبان',
        9: 'رمضان',
        10: 'شوال',
        11: 'ذو القعدة',
        12: 'ذو الحجة',
    }
    for record in self:
        if record.start_date:
            # Day of week (in Arabic) for both form and report
            day_name = arabic_days.get(record.start_date.weekday(), '')
            record.start_date_day_name = day_name
            record.arabic_day = day_name

            # Hijri date conversion
            hijri_value = ''
            if Gregorian:
                hijri = Gregorian(
                    record.start_date.year,
                    record.start_date.month,
                    record.start_date.day
                ).to_hijri()
                hijri_value = f"{hijri.year}/{hijri.month:02d}/{hijri.day:02d}"
            record.start_date_hijri = hijri_value
            record.hijri_date = hijri_value
        else:
            record.start_date_hijri = ''
            record.start_date_day_name = ''
            record.hijri_date = ''
            record.arabic_day = ''
```

### Notes about the logic

- `@api.depends('start_date')` ensures all derived fields recompute when the user changes `start_date`.
- `weekday()` returns `0..6` (Monday..Sunday), so the mapping uses Monday first: `الاثنين`.
- If `hijridate` is not installed, `Gregorian` is `None` and `hijri_value` stays `''`.
- `hijri_months` is defined but not used in the current format; if you want Arabic month names in the output, use it to format the date string.

## Report usage (QWeb)

The report uses the computed fields directly:

```xml
تم في يوم
<span t-field="o.start_date_day_name"/>
بتاريخ
<span t-field="o.start_date_hijri"/>
هـ الموافق
<span t-field="o.start_date"/>
م
```

This means the report is already wired to show:

- Arabic weekday for `start_date`
- Hijri date (YYYY/MM/DD)
- Gregorian date (default Odoo date formatting)

## How to reuse this logic in another Odoo model

1. Add a `Date` field (e.g., `start_date`).
2. Add computed `Char` fields for Hijri and Arabic weekday.
3. Copy the `_compute_date_fields` method (or refactor to a mixin) and adjust field names.
4. Ensure `hijridate` is installed in the Odoo environment.

### Minimal reuse example

```python
try:
    from hijridate import Gregorian
except ImportError:
    Gregorian = None

class MyModel(models.Model):
    _name = 'my.model'

    start_date = fields.Date(string='Start Date')
    hijri_date = fields.Char(compute='_compute_date_fields', store=True)
    arabic_day = fields.Char(compute='_compute_date_fields', store=True)

    @api.depends('start_date')
    def _compute_date_fields(self):
        arabic_days = {
            0: 'الاثنين',
            1: 'الثلاثاء',
            2: 'الأربعاء',
            3: 'الخميس',
            4: 'الجمعة',
            5: 'السبت',
            6: 'الأحد',
        }
        for record in self:
            if record.start_date:
                day_name = arabic_days.get(record.start_date.weekday(), '')
                record.arabic_day = day_name

                hijri_value = ''
                if Gregorian:
                    hijri = Gregorian(
                        record.start_date.year,
                        record.start_date.month,
                        record.start_date.day
                    ).to_hijri()
                    hijri_value = f"{hijri.year}/{hijri.month:02d}/{hijri.day:02d}"
                record.hijri_date = hijri_value
            else:
                record.arabic_day = ''
                record.hijri_date = ''
```

## Optional: Arabic month names in the Hijri output

If you want a format like `12 رمضان 1445`, use the existing month mapping:

```python
hijri_months = {
    1: 'محرم',
    2: 'صفر',
    3: 'ربيع الأول',
    4: 'ربيع الثاني',
    5: 'جمادى الأولى',
    6: 'جمادى الآخرة',
    7: 'رجب',
    8: 'شعبان',
    9: 'رمضان',
    10: 'شوال',
    11: 'ذو القعدة',
    12: 'ذو الحجة',
}

hijri_value = f"{hijri.day} {hijri_months[hijri.month]} {hijri.year}"
```

## Behavior summary

- User selects `start_date` in the form.
- Odoo recomputes and stores `start_date_hijri`, `start_date_day_name`, `hijri_date`, and `arabic_day`.
- Report reads those computed fields directly.
- If the `hijridate` library is missing, Hijri values render empty (no crash).
