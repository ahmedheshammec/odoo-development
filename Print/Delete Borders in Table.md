## Delete Borders in Table

→ Add this in the `css` then call it on the table

```css
.mpnp-header-no-borders,
.mpnp-header-no-borders::before,
.mpnp-header-no-borders::after,
.mpnp-header-no-borders table,
.mpnp-header-no-borders table::before,
.mpnp-header-no-borders table::after,
.mpnp-header-no-borders tbody,
.mpnp-header-no-borders tbody::before,
.mpnp-header-no-borders tbody::after,
.mpnp-header-no-borders tr,
.mpnp-header-no-borders tr::before,
.mpnp-header-no-borders tr::after,
.mpnp-header-no-borders td,
.mpnp-header-no-borders td::before,
.mpnp-header-no-borders td::after,
.mpnp-header-no-borders th,
.mpnp-header-no-borders th::before,
.mpnp-header-no-borders th::after {
    border: none !important;
    border-width: 0 !important;
    border-style: none !important;
    outline: none !important;
    box-shadow: none !important;
}
.mpnp-no-border {
    border: 0 !important;
    outline: 0 !important;
    box-shadow: none !important;
    border-collapse: collapse;
    border-spacing: 0;
}
.mpnp-no-border tr,
.mpnp-no-border th,
.mpnp-no-border td {
    border: 0 !important;
    outline: 0 !important;
    box-shadow: none !important;
}
```

→ Next in the table in xml: 

```xml
<table class="o_ignore_layout_styling mpnp-no-border" border="0" cellpadding="0" cellspacing="0"
       style="width: 100% !important; border: none !important; border-width: 0 !important; border-style: none !important; border-collapse: collapse !important; border-spacing: 0 !important; margin: 0 !important; padding: 0 !important;">
```

→ Next Wrap the table in a borderless container (div)