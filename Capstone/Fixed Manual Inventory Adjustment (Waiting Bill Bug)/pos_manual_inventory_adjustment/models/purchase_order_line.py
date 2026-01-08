from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

# ANSI escape codes
WHITE = "\033[97m"
RESET = "\033[0m"

from ._state import get_skip_po_updates


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def write(self, vals):
        """Debug: Track direct writes to qty_received"""
        if 'qty_received' in vals:
            import traceback
            stack = ''.join(traceback.format_stack()[-5:-1])
            _logger.warning(f"{WHITE}[PO FIX WARNING] Direct write to qty_received: {vals.get('qty_received')} for {len(self)} lines\nStack:\n{stack}{RESET}")
        return super().write(vals)

    @api.depends('move_ids.state', 'move_ids.product_uom', 'move_ids.quantity')
    def _compute_qty_received(self):
        """
        Override to prevent qty_received recalculation when manual inventory
        adjustments are being processed. This ensures that inventory adjustments
        don't affect purchase order billing status.
        """
        context_skip = self.env.context.get('skip_purchase_order_updates')
        param_skip = self.env['ir.config_parameter'].sudo().get_param('pos_manual_inventory_adjustment.skip_po_updates')
        thread_skip = get_skip_po_updates()

        _logger.info(f"{WHITE}[PO FIX DEBUG] context_skip={context_skip}, param_skip={param_skip}, thread_skip={thread_skip}{RESET}")

        skip_updates = (
            context_skip
            or param_skip == '1'
            or thread_skip
        )

        # Also skip if any linked moves are inventory adjustments, regardless of context.
        has_inventory_moves = any(
            move.is_inventory for move in self.mapped('move_ids')
        )

        if skip_updates or has_inventory_moves:
            # Log current values before skipping
            sample_values = [(line.id, line.qty_received) for line in self[:3]]  # Sample first 3
            _logger.info(f"{WHITE}[PO FIX] SKIPPING qty_received computation for {len(self)} PO lines (inventory_move={has_inventory_moves}). Sample values: {sample_values}{RESET}")
            return

        res = super()._compute_qty_received()
        _logger.info(f"{WHITE}[PO FIX] qty_received computed normally for {len(self)} PO lines{RESET}")
        return res

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity', 'qty_received', 'product_uom_qty', 'order_id.state')
    def _compute_qty_invoiced(self):
        """
        Override to prevent qty_invoiced/qty_to_invoice recalculation during inventory adjustments.
        """
        skip_updates = (
            self.env.context.get('skip_purchase_order_updates')
            or self.env['ir.config_parameter'].sudo().get_param('pos_manual_inventory_adjustment.skip_po_updates') == '1'
            or get_skip_po_updates()
        )
        has_inventory_moves = any(
            move.is_inventory for move in self.mapped('move_ids')
        )
        if skip_updates or has_inventory_moves:
            _logger.info(f"{WHITE}[PO FIX] SKIPPING qty_invoiced/qty_to_invoice computation for {len(self)} PO lines (inventory_move={has_inventory_moves}){RESET}")
            return

        res = super()._compute_qty_invoiced()
        _logger.info(f"{WHITE}[PO FIX] qty_invoiced/qty_to_invoice computed normally for {len(self)} PO lines{RESET}")
        return res

    def _get_po_line_moves(self):
        """
        Exclude inventory adjustment moves from PO receipt computations so
        inventory adjustments never alter qty_received on purchase lines.
        """
        moves = super()._get_po_line_moves()
        filtered = moves.filtered(lambda m: not m.is_inventory)
        if len(filtered) != len(moves):
            _logger.info(f"{WHITE}[PO FIX] Ignoring {len(moves) - len(filtered)} inventory moves for qty_received on PO lines{RESET}")
        return filtered
