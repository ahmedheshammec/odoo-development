# Odoo Report Table Styling Guide
## Solutions for Common PDF Report Challenges in Odoo 18

This guide documents solutions for common table styling challenges when creating PDF reports in Odoo using QWeb templates and wkhtmltopdf.

---

## Table of Contents
1. [Removing Outer Table Border While Keeping Inner Table Borders](#1-removing-outer-table-border-while-keeping-inner-table-borders)
2. [Adding Separation Between Side-by-Side Tables](#2-adding-separation-between-side-by-side-tables)
3. [Adding Rounded Corners the Right Way](#3-adding-rounded-corners-the-right-way)

---

## 1. Removing Outer Table Border While Keeping Inner Table Borders

### The Problem
When you have a layout table containing two or more inner tables (e.g., Customer Information and Seller Information side by side), you want:
- **No border** on the outer/wrapper table
- **Borders** on the inner tables only

### The Solution
Use a wrapper table with explicit `border: none !important` and `border-collapse: separate` to ensure no borders appear on the outer structure.

### Code Example

```xml
<!-- Outer wrapper table - NO BORDERS -->
<table border="0" cellpadding="0" cellspacing="0"
       style="width: 100%; border: none !important; border-collapse: separate; border-spacing: 0; margin: 0; padding: 0;">
    <tr style="border: none !important;">

        <!-- Left inner table container -->
        <td style="width: 48%; vertical-align: top; border: none !important;">
            <!-- Inner table WITH border -->
            <table style="width: 100%; border: 1px solid #000; border-collapse: collapse;">
                <tr>
                    <td colspan="4" style="background-color: #d6eaf8; padding: 5px; text-align: center; font-weight: bold;">
                        Customer Information
                    </td>
                </tr>
                <tr>
                    <td style="padding: 3px;">Value 1</td>
                    <td style="padding: 3px;">Label 1</td>
                </tr>
                <!-- More rows... -->
            </table>
        </td>

        <!-- Middle spacer (optional) -->
        <td style="width: 4%; border: none !important;"></td>

        <!-- Right inner table container -->
        <td style="width: 48%; vertical-align: top; border: none !important;">
            <!-- Inner table WITH border -->
            <table style="width: 100%; border: 1px solid #000; border-collapse: collapse;">
                <tr>
                    <td colspan="4" style="background-color: #d6eaf8; padding: 5px; text-align: center; font-weight: bold;">
                        Seller Information
                    </td>
                </tr>
                <tr>
                    <td style="padding: 3px;">Value 1</td>
                    <td style="padding: 3px;">Label 1</td>
                </tr>
                <!-- More rows... -->
            </table>
        </td>

    </tr>
</table>
```

### Key Points

| Element | Style | Purpose |
|---------|-------|---------|
| Outer `<table>` | `border: none !important` | Removes any border |
| Outer `<table>` | `border-collapse: separate` | Prevents border inheritance |
| Outer `<table>` | `border="0" cellpadding="0" cellspacing="0"` | HTML attributes for extra safety |
| Outer `<tr>` | `border: none !important` | Ensures row has no border |
| Outer `<td>` | `border: none !important` | Ensures cells have no border |
| Inner `<table>` | `border: 1px solid #000` | The visible border you want |

### Why `!important`?
Odoo's default CSS and wkhtmltopdf may apply unexpected borders. Using `!important` ensures your styles take precedence.

---

## 2. Adding Separation Between Side-by-Side Tables

### The Problem
You have two tables side by side (e.g., Delivery Cost and Totals) and want a visible gap/space between them.

### The Solution
Add an empty `<td>` element between the two table containers with a percentage width.

### Code Example

```xml
<table border="0" cellpadding="0" cellspacing="0"
       style="width: 100%; border: none !important; border-collapse: separate; border-spacing: 0;">
    <tr style="border: none !important;">

        <!-- Left table (48% width) -->
        <td style="width: 48%; vertical-align: top; border: none !important;">
            <div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px; text-align: center; font-weight: bold;">
                            Delivery Cost
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px; text-align: center;">
                            Some content here...
                        </td>
                    </tr>
                </table>
            </div>
        </td>

        <!-- MIDDLE SPACER - Creates the gap -->
        <td style="width: 4%; border: none !important;"></td>

        <!-- Right table (48% width) -->
        <td style="width: 48%; vertical-align: top; border: none !important;">
            <div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px; text-align: center;">
                            Total Amount
                        </td>
                        <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;">
                            Label
                        </td>
                    </tr>
                </table>
            </div>
        </td>

    </tr>
</table>
```

### Width Distribution

| Element | Width | Description |
|---------|-------|-------------|
| Left table | 48% | First table container |
| Middle spacer | 4% | Empty gap between tables |
| Right table | 48% | Second table container |
| **Total** | **100%** | Must equal 100% |

### Alternative: Using Padding
Instead of a middle `<td>`, you can add padding to the table containers:

```xml
<td style="width: 50%; vertical-align: top; border: none !important; padding-right: 10px;">
    <!-- Left table -->
</td>
<td style="width: 50%; vertical-align: top; border: none !important; padding-left: 10px;">
    <!-- Right table -->
</td>
```

---

## 3. Adding Rounded Corners the Right Way

### The Problem
`border-radius` on `<table>` elements doesn't work properly in wkhtmltopdf (Odoo's PDF renderer). The corners appear square even when you set `border-radius: 8px`.

### The Solution
Wrap the table in a `<div>` that has the border and border-radius, then remove the border from the table itself.

### Basic Implementation

```xml
<!-- CORRECT: Wrapper div with border-radius -->
<div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="border: 1px solid #000; padding: 5px;">Cell 1</td>
            <td style="border: 1px solid #000; padding: 5px;">Cell 2</td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; padding: 5px;">Cell 3</td>
            <td style="border: 1px solid #000; padding: 5px;">Cell 4</td>
        </tr>
    </table>
</div>
```

### Key CSS Properties for the Wrapper Div

```css
border: 1px solid #000;      /* The visible outer border */
border-radius: 8px;          /* Rounded corners */
overflow: hidden;            /* CRITICAL: Clips content to rounded shape */
```

### Handling Background Colors

#### The Problem
When cells have background colors, the color extends to the edges and covers the rounded corners, making them appear square again.

#### The Solution
Add matching `border-radius` to the corner cells that have background colors.

### Complete Example with Background Colors

```xml
<div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
    <table style="width: 100%; border-collapse: collapse;">
        <!-- Header row with background color -->
        <tr>
            <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;
                       border-top-left-radius: 8px;">
                Header Left
            </td>
            <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;
                       border-top-right-radius: 8px;">
                Header Right
            </td>
        </tr>

        <!-- Middle rows - no border-radius needed -->
        <tr>
            <td style="border: 1px solid #000; padding: 5px;">Middle Left</td>
            <td style="border: 1px solid #000; padding: 5px;">Middle Right</td>
        </tr>

        <!-- Bottom row -->
        <tr>
            <td style="border: 1px solid #000; padding: 5px;
                       border-bottom-left-radius: 8px;">
                Bottom Left
            </td>
            <td style="border: 1px solid #000; padding: 5px;
                       border-bottom-right-radius: 8px;">
                Bottom Right
            </td>
        </tr>
    </table>
</div>
```

### Corner Cell Border-Radius Reference

| Cell Position | CSS Property |
|---------------|--------------|
| Top-Left | `border-top-left-radius: 8px;` |
| Top-Right | `border-top-right-radius: 8px;` |
| Bottom-Left | `border-bottom-left-radius: 8px;` |
| Bottom-Right | `border-bottom-right-radius: 8px;` |

### Special Case: Single Column Tables

For tables with only one column, the corner cells span the full width:

```xml
<div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <!-- First row: both top corners -->
            <td style="border: 1px solid #000; padding: 5px;
                       border-top-left-radius: 8px; border-top-right-radius: 8px;">
                Header
            </td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; padding: 5px;">Middle Row</td>
        </tr>
        <tr>
            <!-- Last row: both bottom corners -->
            <td style="border: 1px solid #000; padding: 5px;
                       border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                Footer
            </td>
        </tr>
    </table>
</div>
```

### Special Case: Colspan Header

When a header row uses `colspan` to span all columns:

```xml
<div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <!-- Header with colspan: needs BOTH top corners -->
            <td colspan="4" style="background-color: #d6eaf8; padding: 5px;
                                   border-top-left-radius: 8px; border-top-right-radius: 8px;">
                Table Header
            </td>
        </tr>
        <tr>
            <td style="padding: 3px;">Col 1</td>
            <td style="padding: 3px;">Col 2</td>
            <td style="padding: 3px;">Col 3</td>
            <td style="padding: 3px;">Col 4</td>
        </tr>
        <!-- More rows... -->
        <tr>
            <!-- Last row: individual corner cells -->
            <td style="padding: 3px; border-bottom-left-radius: 8px;">Bottom Left</td>
            <td style="padding: 3px;">Col 2</td>
            <td style="padding: 3px;">Col 3</td>
            <td style="padding: 3px; border-bottom-right-radius: 8px;">Bottom Right</td>
        </tr>
    </table>
</div>
```

### Special Case: RTL (Right-to-Left) Tables

For RTL tables (`direction: rtl`), the visual layout is mirrored but CSS properties remain the same:

- First `<td>` in HTML = **Right side** visually
- Last `<td>` in HTML = **Left side** visually

```xml
<div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
    <table style="width: 100%; border-collapse: collapse; direction: rtl;">
        <tr>
            <!-- First td (appears on RIGHT in RTL) -->
            <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;
                       border-top-right-radius: 8px;">
                Right Header (First in HTML)
            </td>
            <td style="border: 1px solid #000; padding: 5px;">Middle</td>
            <!-- Last td (appears on LEFT in RTL) -->
            <td style="border: 1px solid #000; padding: 5px;
                       border-top-left-radius: 8px;">
                Left Header (Last in HTML)
            </td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;
                       border-bottom-right-radius: 8px;">
                Right Footer
            </td>
            <td style="border: 1px solid #000; padding: 5px;">Middle</td>
            <td style="border: 1px solid #000; padding: 5px;
                       border-bottom-left-radius: 8px;">
                Left Footer
            </td>
        </tr>
    </table>
</div>
```

### RTL Corner Mapping

| Visual Position | HTML Position | Border-Radius Property |
|-----------------|---------------|------------------------|
| Top-Right | First td, first row | `border-top-right-radius` |
| Top-Left | Last td, first row | `border-top-left-radius` |
| Bottom-Right | First td, last row | `border-bottom-right-radius` |
| Bottom-Left | Last td, last row | `border-bottom-left-radius` |

---

## Quick Reference Checklist

### For Borderless Outer Tables:
- [ ] Add `border="0" cellpadding="0" cellspacing="0"` to outer table
- [ ] Add `border: none !important` to outer table style
- [ ] Add `border-collapse: separate` to outer table
- [ ] Add `border: none !important` to all outer `<tr>` and `<td>`

### For Table Separation:
- [ ] Use percentage widths that total 100%
- [ ] Add empty `<td>` spacer with desired width (e.g., 4%)
- [ ] Set `border: none !important` on spacer

### For Rounded Corners:
- [ ] Wrap table in `<div>` with border-radius
- [ ] Add `overflow: hidden` to the div
- [ ] Remove border from table, keep on div
- [ ] Add matching border-radius to corner cells with background colors
- [ ] For RTL tables, remember first td = right side visually

---

## Complete Working Example

Here's a complete example combining all techniques:

```xml
<!-- Two side-by-side tables with rounded corners and proper borders -->
<table border="0" cellpadding="0" cellspacing="0"
       style="width: 100%; border: none !important; border-collapse: separate; border-spacing: 0;">
    <tr style="border: none !important;">

        <!-- Left Table -->
        <td style="width: 48%; vertical-align: top; border: none !important;">
            <div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;
                                   border-top-left-radius: 8px; border-top-right-radius: 8px;
                                   text-align: center; font-weight: bold;">
                            Left Table Header
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px;">Content Row 1</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px;
                                   border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                            Content Row 2
                        </td>
                    </tr>
                </table>
            </div>
        </td>

        <!-- Spacer -->
        <td style="width: 4%; border: none !important;"></td>

        <!-- Right Table -->
        <td style="width: 48%; vertical-align: top; border: none !important;">
            <div style="border: 1px solid #000; border-radius: 8px; overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px; border-top-left-radius: 8px;">
                            Value
                        </td>
                        <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;
                                   border-top-right-radius: 8px;">
                            Label
                        </td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px; border-bottom-left-radius: 8px;">
                            Value
                        </td>
                        <td style="border: 1px solid #000; padding: 5px; background-color: #d6eaf8;
                                   border-bottom-right-radius: 8px;">
                            Label
                        </td>
                    </tr>
                </table>
            </div>
        </td>

    </tr>
</table>
```

---

*Documentation created for Odoo 18 PDF Report Development*
*Last updated: January 2026*
