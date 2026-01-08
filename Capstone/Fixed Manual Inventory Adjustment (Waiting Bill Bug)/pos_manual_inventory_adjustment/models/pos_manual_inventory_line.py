from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from ._state import set_skip_po_updates, get_skip_po_updates
import logging

_logger = logging.getLogger(__name__)
WHITE = "\033[97m"
RESET = "\033[0m"


class PosManualInventoryLine(models.Model):
    _name = 'pos.manual.inventory.line'
    _description = 'POS Manual Inventory Line'
    _rec_name = 'product_id'

    inventory_id = fields.Many2one(
        'pos.manual.inventory',
        string='Inventory Adjustment',
        required=True,
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )

    product_barcode = fields.Char(
        related='product_id.barcode',
        string='Barcode',
        readonly=True
    )

    product_uom_id = fields.Many2one(
        related='product_id.uom_id',
        string='Unit of Measure',
        readonly=True
    )

    theoretical_qty = fields.Float(
        string='Theoretical Quantity',
        compute='_compute_theoretical_qty',
        store=True,
        readonly=True
    )

    counted_qty = fields.Float(
        string='Counted Quantity',
        default=0.0,
        required=True
    )

    difference = fields.Float(
        string='Difference',
        compute='_compute_difference',
        store=True,
        readonly=True
    )

    location_id = fields.Many2one(
        related='inventory_id.location_id',
        string='Location',
        readonly=True
    )

    state = fields.Selection(
        related='inventory_id.state',
        string='Status',
        readonly=True
    )

    is_auto_populated = fields.Boolean(
        string='Auto Populated',
        default=False,
        help='True if this line was created by Request Count, False if manually added'
    )



    @api.depends('product_id', 'location_id')
    def _compute_theoretical_qty(self):
        """Compute theoretical quantity from stock quants"""
        for line in self:
            if line.product_id and line.location_id:
                quant = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.location_id.id)
                ], limit=1)
                line.theoretical_qty = quant.quantity if quant else 0.0
            else:
                line.theoretical_qty = 0.0

    @api.depends('theoretical_qty', 'counted_qty')
    def _compute_difference(self):
        """Compute difference between counted and theoretical quantities"""
        for line in self:
            line.difference = line.counted_qty - line.theoretical_qty

    @api.constrains('counted_qty')
    def _check_counted_qty(self):
        """Validate counted quantity"""
        for line in self:
            if line.counted_qty < 0:
                raise ValidationError(_("Counted quantity cannot be negative."))

    @api.constrains('product_id')
    def _check_product_type(self):
        """Validate that only stockable products can be added"""
        for line in self:
            if line.product_id and line.product_id.type != 'product':
                raise ValidationError(_("Only stockable products can be added to inventory adjustments. The product '%s' will be automatically converted to stockable type.") % line.product_id.name)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Reset counted quantity when product changes and ensure product is storable"""
        if self.product_id:
            self.counted_qty = 0.0
            # Ensure the product is storable (type should be 'product' for stockable)
            if self.product_id.type in ['consu', 'service']:
                try:
                    # Avoid triggering PO recomputations while updating product type
                    self.product_id.sudo().with_context(skip_purchase_order_updates=True).write({'type': 'product'})
                except Exception:
                    # If we can't change the type, show a warning
                    pass

    @api.model
    def create(self, vals):
        """Override create to ensure product is storable and prevent PO updates"""
        # Set global flag BEFORE creating the line
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('pos_manual_inventory_adjustment.skip_po_updates', '1')
        set_skip_po_updates(True)

        if 'product_id' in vals and vals['product_id']:
            product = self.env['product.product'].browse(vals['product_id'])
            if product.type in ['consu', 'service']:
                try:
                    product.sudo().with_context(skip_purchase_order_updates=True).write({'type': 'product'})
                except Exception:
                    # If we can't change the type, let validation handle it
                    pass

        _logger.info(f"{WHITE}[PO FIX] Creating inventory line with global protection enabled{RESET}")
        result = super(PosManualInventoryLine, self.with_context(skip_purchase_order_updates=True)).create(vals)

        # DO NOT clear the flags immediately - let them persist for the computed fields
        # The flags will be cleared when the user moves away from the inventory form
        _logger.info(f"{WHITE}[PO FIX] Inventory line created (ID={result.id}), keeping protection active{RESET}")
        return result

    def write(self, vals):
        """Override write to ensure product is storable and prevent PO updates"""
        # Set global flag BEFORE updating the line
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('pos_manual_inventory_adjustment.skip_po_updates', '1')
        set_skip_po_updates(True)

        if 'product_id' in vals and vals['product_id']:
            product = self.env['product.product'].browse(vals['product_id'])
            if product.type in ['consu', 'service']:
                try:
                    product.sudo().with_context(skip_purchase_order_updates=True).write({'type': 'product'})
                except Exception:
                    # If we can't change the type, let validation handle it
                    pass

        _logger.info(f"{WHITE}[PO FIX] Updating inventory line with global protection enabled{RESET}")
        result = super(PosManualInventoryLine, self.with_context(skip_purchase_order_updates=True)).write(vals)

        # DO NOT clear the flags - let them persist
        _logger.info(f"{WHITE}[PO FIX] Inventory line updated, keeping protection active{RESET}")
        return result
