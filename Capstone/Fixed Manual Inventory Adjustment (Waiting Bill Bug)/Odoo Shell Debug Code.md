```py
# Odoo shell
orders = env['purchase.order'].search([('invoice_status', '=', 'to invoice')])
orders.write({'invoice_status': 'invoiced'})
print("Updated:", len(orders))
commit()
```

```py
po = env['purchase.order'].browse(5922)

if po.exists():
    count = 0
    for line in po.order_line:
        line.write({'qty_received': 100})
        count += 1
    print(f"Updated {count} PO lines for PO {po.name} (ID 5922)")
else:
    print("PO not found.")
commit()

```

id = 5922