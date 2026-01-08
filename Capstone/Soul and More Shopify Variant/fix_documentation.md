Fix Documentation

Summary
- Added REST-based pagination for Shopify variants to ensure products with >100 variants sync all variants.
- Expanded the Shopify product payload's variants list before sync so counts and variant processing reflect full data.

Files Changed
- shopify_ept/models/shopify_template_ept.py

Code Snippets Added

1) Expand variants in the product payload before sync

Location: shopify_ept/models/shopify_template_ept.py (convert_shopify_template_response)

```python
        template_id = template_data.get("id") if template_data else False
        if template_id:
            existing_variants = template_data.get("variants") or []
            full_variants = self._fetch_all_variants_from_shopify(template_id)
            if full_variants and len(full_variants) >= len(existing_variants):
                if len(full_variants) != len(existing_variants):
                    _logger.info(
                        "Expanded variants for product %s from %s to %s.",
                        template_id, len(existing_variants), len(full_variants)
                    )
                template_data["variants"] = full_variants
```

2) Fetch all variants using REST pagination

Location: shopify_ept/models/shopify_template_ept.py (_fetch_all_variants_from_shopify)

```python
    def _fetch_all_variants_from_shopify(self, template_id):
        variants = []
        try:
            results = shopify.Variant().find(product_id=template_id, limit=250)
        except ClientError as error:
            if hasattr(error, "response") and error.response.code == 429 and error.response.msg == "Too Many Requests":
                time.sleep(int(float(error.response.headers.get('Retry-After', 5))))
                results = shopify.Variant().find(product_id=template_id, limit=250)
            else:
                _logger.info("Failed to fetch variants for product %s. Error: %s", template_id, str(error))
                return variants
        except Exception as error:
            _logger.info("Failed to fetch variants for product %s. Error: %s", template_id, str(error))
            return variants

        if not results:
            return variants

        variants += [variant.to_dict() if not isinstance(variant, dict) else variant for variant in results]

        catch = ""
        while results:
            page_info = ""
            link = (results.metadata.get('headers', {}).get('Link') or
                    results.metadata.get('headers', {}).get('link') or
                    shopify.ShopifyResource.connection.response.headers.get('Link') or
                    shopify.ShopifyResource.connection.response.headers.get('link'))
            if not link or not isinstance(link, str):
                break
            for page_link in link.split(","):
                if page_link.find("next") > 0:
                    page_info = page_link.split(";")[0].strip("<>").split("page_info=")[1]
                    try:
                        results = shopify.Variant().find(product_id=template_id, page_info=page_info, limit=250)
                        variants += [variant.to_dict() if not isinstance(variant, dict) else variant for variant in results]
                    except ClientError as error:
                        if hasattr(error,
                                   "response") and error.response.code == 429 and error.response.msg == "Too Many Requests":
                            time.sleep(int(float(error.response.headers.get('Retry-After', 5))))
                            results = shopify.Variant().find(product_id=template_id, page_info=page_info, limit=250)
                            variants += [variant.to_dict() if not isinstance(variant, dict) else variant
                                         for variant in results]
                        else:
                            _logger.info("Failed to fetch variants for product %s. Error: %s", template_id, str(error))
                            return variants
                    except Exception as error:
                        _logger.info("Failed to fetch variants for product %s. Error: %s", template_id, str(error))
                        return variants
            if catch == page_info:
                break
            catch = page_info

        return variants
```

Notes
- This uses the REST endpoint `/products/{id}/variants.json` with `limit=250` and cursor pagination.
- No GraphQL changes were made.
