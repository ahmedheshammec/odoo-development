from odoo import models
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def unlink(self):
        for record in self:
            _logger.info(f"Bypassing Shopify unlink: {record.id}")
        return models.Model.unlink(self)
