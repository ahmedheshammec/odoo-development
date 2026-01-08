# Bosta Delivery

======================================================================
Carrier Name: Bosta Delivery
Bosta API Key: 359b0b5674b353247d54f1b90ea8c84814ba008394136931f999786dfc5823e8
Bosta API URL: https://api.bosta.co/api/v0
Bosta Tracking Endpoint: https://bosta.co/tracking-shipments?shipment-number=

Active: True

======================================================================
Carrier Name: Bosta exchange
Bosta API Key: 359b0b5674b353247d54f1b90ea8c84814ba008394136931f999786dfc5823e8
Bosta API URL: https://api.bosta.co/api/v0
Bosta Tracking Endpoint: https://bosta.co/tracking-shipments?shipment-number=

Active: True

---

⏺ Looking at the code, YES, the notes ARE being sent in TWO places in the payload:

  1. Inside packageDetails.description (lines 125-129):
    package_details = {
      "itemsCount": item_count,
      "document": "Document",
      "description": shipment_data.get('notes')  # ← FIRST PLACE
    }

  2. At the top-level notes field (line 148):
    shipment = {
      "specs": {
          "size": "SMALL",
          "packageDetails": package_details  # Contains description with notes
      },
      ...
      'notes': delivery_note,  # ← SECOND PLACE (line 148)
      ...
    }

  Where:
  - Line 102: shipment_data = ctx.get("vals_for_shipping")
  - Line 75: delivery_vals = ctx.get('vals_for_shipping')
  - Line 136: delivery_note = delivery_vals.get('notes', '')

---

```json
curl --request POST \
  --url "https://app.bosta.co/api/v2/deliveries" \
  --header "Authorization: 359b0b5674b353247d54f1b90ea8c84814ba008394136931f999786dfc5823e8" \
  --header "Content-Type: application/json" \
  --data '{
    "type": 10,
    "specs": {
      "packageType": "Parcel",
      "size": "SMALL",
      "packageDetails": {
        "itemsCount": 1,
        "description": "Test package"
      }
    },
    "dropOffAddress": {
      "cityCode": "EG-01",
      "zoneId": "oTL8FAlzHa",
      "firstLine": "Test Street",
      "secondLine": "Building 12",
      "buildingNumber": "12",
      "floor": 3,
      "apartment": "5"
    },
    "receiver": {
      "firstName": "Test",
      "lastName": "User",
      "phone": "01012345678",
      "email": "test@example.com"
    },
    "cod": 0,
    "notes": "00000000000001111111"
  }'
```

Changed: "packageType": "Package" → "packageType": "Parcel"

  Valid values are:
  - "Parcel"
  - "Document"
  - "Light Bulky"
  - "Heavy Bulky"
  
    Changed: "zoneId": "10" → "zoneId": "oTL8FAlzHa" (ElMaadi zone)

  Other valid Cairo zones you can use:
  - "NQz5sDOeG" - Helwan
  - "g3jl3V8FMN" - New Cairo
  - "3wlBON0dNs" - ElZamalek
  - "X8cQwam6-4" - Qasr ElNile

  This should work now with your barcode in the notes field! 🎯

→ Response: 

```json
{
  "success": true,
  "message": "Done successfully.",
  "data": {
    "_id": "N10ZIy8s5Blz2p36khM4N",
    "trackingNumber": "80160611",
    "sender": {
      "_id": "oXx2EVousA2YqgzUqlmeL",
      "phone": "+201016600244",
      "name": "Soulandmore",
      "type": "BUSINESS_ACCOUNT",
      "subAccountId": null
    },
    "message": "Delivery created successfully!",
    "state": {
      "code": 10,
      "value": "Pickup requested"
    },
    "creationSrc": "API"
  }
}
```

