from odoo import models, api
from ._state import get_skip_po_updates
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Ensure inventory adjustment moves are never linked to purchase order lines.
        If skip flag is present or the move is marked as inventory, strip any
        purchase_line_id to avoid touching PO qty_received/invoice status.
        """
        skip_context = self.env.context.get('skip_purchase_order_updates') or get_skip_po_updates()
        for vals in vals_list:
            is_inventory = vals.get('is_inventory') or self.env.context.get('inventory_mode')
            if skip_context or is_inventory:
                if vals.get('purchase_line_id'):
                    _logger.info("Removing purchase_line_id from inventory move to protect PO updates")
                vals.pop('purchase_line_id', None)
        return super().create(vals_list)

    def _action_done(self, cancel_backorder=False):
        """
        Override to prevent purchase order updates during manual inventory adjustments.
        When skip_purchase_order_updates context is set, we ensure that inventory
        adjustment moves don't trigger purchase order line qty_received recalculations.
        """
        if self.env.context.get('skip_purchase_order_updates') or get_skip_po_updates():
            # Apply the skip context to all moves in this batch to be safe
            return super(StockMove, self.with_context(skip_purchase_order_updates=True))._action_done(
                cancel_backorder=cancel_backorder
            )

        return super()._action_done(cancel_backorder=cancel_backorder)
