from . import models

from openupgradelib import openupgrade


def _sale_commission_pricelist_oca_pre_init_hook(env):
    if openupgrade.table_exists(env.cr, "sale_commission_pricelist"):
        modules = [("sale_commission_pricelist", "sale_commission_pricelist_oca")]
        openupgrade.update_module_names(env.cr, modules, merge_modules=True)
