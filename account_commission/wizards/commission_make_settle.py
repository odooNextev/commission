# Copyright 2014-2022 Tecnativa - Pedro M. Baeza
# Copyright 2022 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class CommissionMakeSettle(models.TransientModel):
    _inherit = "commission.make.settle"

    settlement_type = fields.Selection(
        selection_add=[("sale_invoice", "Sales Invoices")],
        ondelete={"sale_invoice": "cascade"},
    )
    date_payment_to = fields.Date(
        "Payment date up to",
        help="For payment-based commissions, settlements will be created for payments \
            with date up to the one set in this field.",
        default=fields.Date.today,
    )

    def _get_account_settle_domain(self, agent, date_to_agent):
        return [
            ("invoice_date", "<", date_to_agent),
            ("agent_id", "=", agent.id),
            ("settled", "=", False),
            ("object_id.display_type", "=", "product"),
        ]

    def _get_agent_lines(self, agent, date_to_agent):
        """Filter sales invoice agent lines for this type of settlement."""
        if self.settlement_type != "sale_invoice":
            return super()._get_agent_lines(agent, date_to_agent)

        lines = self.env["account.invoice.line.agent"].search(
            self._get_account_settle_domain(agent, date_to_agent)
        )

        if agent.commission_id.settled_dates_based_on == "payment":
            invoices = lines.mapped("invoice_id")
            payment_date_by_inv = {}

            for inv in invoices:
                invoice_partials, _ = inv._get_reconciled_invoices_partials()
                dates = [
                    cp_line.date
                    for _p, _amt, cp_line in invoice_partials
                    if cp_line.date
                ]
                if dates:
                    payment_date_by_inv[inv.id] = max(dates)

            # Filtra solo le righe con fatture che hanno pagamenti entro date_payment_to
            lines = lines.filtered(lambda l: l.invoice_id.id in payment_date_by_inv)

            return lines.sorted(
                key=lambda l: (
                    payment_date_by_inv.get(l.invoice_id.id),
                    l.id,
                )
            )

        return lines.sorted(key=lambda l: (l.invoice_date, l.id))

    def _prepare_settlement_line_vals(self, settlement, line):
        """Prepare extra settlement values when the source is a sales invoice agent
        line.
        """
        res = super()._prepare_settlement_line_vals(settlement, line)
        if self.settlement_type == "sale_invoice":
            res.update(
                {
                    "invoice_agent_line_id": line.id,
                    "date": line.invoice_date,
                    "commission_id": line.commission_id.id,
                    "settled_amount": line.amount,
                }
            )
        return res

    def action_settle(self):
        self = self.with_context(date_payment_to=self.date_payment_to)
        return super().action_settle()

    def get_period_date(self, line):
        if line.agent_id.commission_id.settled_dates_based_on != "payment":
            return super().get_period_date(line)
        return self.get_latest_payment_date(line.invoice_id)

    def get_latest_payment_date(self, invoice):
        """Get the latest payment date for an invoice."""
        payments_dates = []
        (
            invoice_partials,
            exchange_diff_moves,
        ) = invoice._get_reconciled_invoices_partials()
        for (
            _partial,
            _amount,
            counterpart_line,
        ) in invoice_partials:
            payments_dates.append(counterpart_line.date)
        return max(payments_dates) if payments_dates else invoice.invoice_date
