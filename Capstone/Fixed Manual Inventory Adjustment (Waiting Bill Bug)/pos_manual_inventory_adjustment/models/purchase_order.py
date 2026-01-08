from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

# ANSI escape codes
WHITE = "\033[97m"
RESET = "\033[0m"

from ._state import get_skip_po_updates


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def read(self, fields=None, load='_classic_read'):
        """Clear the global flag when reading PO (opening the form)"""
        ICP = self.env['ir.config_parameter'].sudo()
        param_skip = ICP.get_param('pos_manual_inventory_adjustment.skip_po_updates', '0')

        # Only clear if flag is set and we're opening a PO form (not inventory operations)
        if param_skip == '1' and not self.env.context.get('skip_purchase_order_updates'):
            _logger.info(f"{WHITE}[PO FIX] Clearing global flag when opening PO form{RESET}")
            ICP.set_param('pos_manual_inventory_adjustment.skip_po_updates', '0')

        return super().read(fields=fields, load=load)

    @api.depends('state', 'order_line.qty_to_invoice')
    def _get_invoiced(self):
        """
        Override to prevent invoice_status recalculation when manual inventory
        adjustments are being processed. This ensures that inventory adjustments
        don't affect purchase order billing status.
        """
        skip_updates = (
            self.env.context.get('skip_purchase_order_updates')
            or self.env['ir.config_parameter'].sudo().get_param('pos_manual_inventory_adjustment.skip_po_updates') == '1'
            or get_skip_po_updates()
        )
        if skip_updates:
            _logger.info(f"{WHITE}[PO FIX] SKIPPING invoice_status computation for {len(self)} POs{RESET}")
            return

        res = super()._get_invoiced()
        _logger.info(f"{WHITE}[PO FIX] invoice_status computed normally for {len(self)} POs{RESET}")
        return res
