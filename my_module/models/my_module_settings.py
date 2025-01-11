from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    birthday = fields.Datetime(string='Birthday Date', help="Birthday Date", config_parameter='my_module.birthday')