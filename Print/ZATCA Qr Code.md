# ZATCA Qr Code

→ First Do this:

```bash
brew install cairo pkg-config
cd-odoo18
source .venv/bin/activate
pip install pycairo rlPyCairo
```

→ Next restart the server and print the pdf again. you can also see the qr directly from the browser url like this: 

```
http://127.0.0.1:8069/report/barcode/?barcode_type=QR&value=test&width=300&height=300
```

## Code Snippet: 

```xml
<img t-if="o.l10n_sa_qr_code_str" style="width:140px; height:140px;"
     t-att-src="'/report/barcode/?barcode_type=%s&amp;value=%s&amp;width=%s&amp;height=%s'%('QR', quote_plus(o.l10n_sa_qr_code_str), 150, 150)"/>
```

→ Control the Qr Code Size with this `style="width:140px; height:140px;"`

