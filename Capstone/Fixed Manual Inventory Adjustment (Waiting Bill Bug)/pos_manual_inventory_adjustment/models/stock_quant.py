from odoo import models
from ._state import get_skip_po_updates
import logging

_logger = logging.getLogger(__name__)

# ANSI escape codes
WHITE = "\033[97m"
RESET = "\033[0m"


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _apply_inventory(self):
        """
        Override to ensure that inventory adjustments from POS manual inventory
        don't trigger purchase order updates. We propagate the skip_purchase_order_updates
        context through the entire inventory adjustment flow.
        """
        skip_updates = (
            self.env.context.get('skip_purchase_order_updates')
            or self.env['ir.config_parameter'].sudo().get_param('pos_manual_inventory_adjustment.skip_po_updates') == '1'
            or get_skip_po_updates()
        )

        if skip_updates:
            _logger.info(f"{WHITE}[PO FIX] Applying inventory with skip_purchase_order_updates context{RESET}")
            # Ensure the context is propagated to stock move creation and _action_done
            return super(StockQuant, self.with_context(skip_purchase_order_updates=True))._apply_inventory()

        return super()._apply_inventory()
