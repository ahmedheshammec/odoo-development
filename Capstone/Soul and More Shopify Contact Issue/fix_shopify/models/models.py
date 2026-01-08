from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def set_delivery_line(self, carrier, price_unit):
        for order in self:
            delivery_lines = order.order_line.filtered(lambda l: l.is_delivery)

            for line in delivery_lines:
                if line.shopify_line_id:
                    # Ensure the line has a product; if not, raise a UserError
                    if not line.product_id:
                        raise UserError(
                            "A delivery line must have a product assigned before confirming the sale order.")

                    # Update the line with price_unit and carrier name
                    line.write({
                        'price_unit': price_unit,
                        'name': carrier.name
                    })

                    if carrier.route_ids:
                        line.write({'route_id': carrier.route_ids[0].id})

                    return

            # If no shopify_line_id delivery line is found, call the super method
            result = super(SaleOrder, order).set_delivery_line(carrier, price_unit)

            # After calling super, apply the route to the new delivery line if created
            delivery_lines = order.order_line.filtered(lambda l: l.is_delivery)
            if delivery_lines and carrier.route_ids:
                # Ensure the line has a product before applying the route
                if not delivery_lines[-1].product_id:
                    raise UserError("A delivery line must have a product assigned before confirming the sale order.")

                delivery_lines[-1].write({'route_id': carrier.route_ids[0].id})

            return result
