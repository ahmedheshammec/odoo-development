# Bubblzz Contact Migration Plan

## Recommended Solution: Use External IDs (XML IDs)

The most robust approach is to use Odoo's **external ID system** (`ir.model.data`). Here's how:

→ Odoo 15 Query

```sql
SELECT DISTINCT
    rp.id,
    'odoo15_partner_' || rp.id AS external_id,  -- Create unique external ID
    rp.name,
    CASE
        WHEN rp.is_company THEN 'company'
        ELSE 'person'
    END AS company_type,
    rp.parent_id,
    'odoo15_partner_' || rp.parent_id AS parent_external_id,  -- External ID for parent

    rp.parent_id,
    rp.phone,
    rp.mobile,
    rp.email,
    rp.website,
    rp.title,
    rp.function,
    rp.vat,
    rp.ref,
    rp.state_id,
    rp.street,
    rp.street2,
    rp.city,
    rp.country_id,
    rp.zip,
    rp.birth_date,

    aar.code AS receivable_account_code,
    aap.code AS payable_account_code

FROM res_partner rp

JOIN account_move am
    ON am.partner_id = rp.id

-- Receivable property
LEFT JOIN ir_property ipr
    ON ipr.name = 'property_account_receivable_id'
   AND ipr.res_id = 'res.partner,' || rp.id

LEFT JOIN account_account aar
    ON aar.id = split_part(ipr.value_reference, ',', 2)::int

-- Payable property
LEFT JOIN ir_property ipp
    ON ipp.name = 'property_account_payable_id'
   AND ipp.res_id = 'res.partner,' || rp.id

LEFT JOIN account_account aap
    ON aap.id = split_part(ipp.value_reference, ',', 2)::int

WHERE am.move_type = 'out_invoice'
  AND am.state = 'posted'
  AND (
        (rp.phone IS NOT NULL AND length(regexp_replace(rp.phone, '\D', '', 'g')) >= 9)
     OR (rp.mobile IS NOT NULL AND length(regexp_replace(rp.mobile, '\D', '', 'g')) >= 9)
  );


```

### During import in Odoo 18:

- Import in two passes:
  - **First pass**: Import all companies (where `parent_id` IS NULL)
  - **Second pass**: Import contacts with parent relationships
- Use the external ID mapping to link parents:
  - When importing, specify the `external_id` field
  - For `parent_id`, reference the parent's external ID instead of the numeric ID
  - Odoo will automatically resolve the reference

```shell
./odoo-bin shell -c "/Volumes/Samsung T5/Odoo/Odoo/Capstone/18/cs_18_dev/cs_18_dev.conf" -d cs_18_dev --no-http < "/Volumes/Samsung T5/Odoo/Odoo/Capstone/18/cs_18_dev/custom cs_18_dev/run_import.py"
```



