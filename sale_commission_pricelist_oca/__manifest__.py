# Copyright 2018 Carlos Dauden - Tecnativa <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sales commissions by pricelist OCA",
    "version": "18.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA), ArcheTI",
    "category": "Sales Management",
    "website": "https://github.com/OCA/commission",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
    "depends": ["sale_commission_oca"],
    "data": ["views/product_pricelist_view.xml"],
    "pre_init_hook": "_sale_commission_pricelist_oca_pre_init_hook",
    "installable": True,
}
