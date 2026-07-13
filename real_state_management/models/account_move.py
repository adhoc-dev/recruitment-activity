import logging

from odoo import Command, api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _generate_estate_accounting_data(self):
        """Genera asientos contables de ejemplo para la actividad de reclutamiento.

        Crea tres asientos, todos POSTEADOS (state='posted') y con ref
        "Actividad" para poder filtrarlos facil en la vista:
          1. Uno correcto (debe == haber), a modo de contraste.
          2. Uno DELIBERADAMENTE descuadrado. Se arma balanceado con el ORM, se
             postea (para pasar la validacion ``_check_balanced``) y recien
             despues se rompe el balance con un ``UPDATE`` SQL directo, salteando
             esa validacion.
          3. Uno de venta con el IVA mal liquidado: cuadra, pero el IVA declarado
             no se corresponde con la base imponible.

        La intencion es que quien resuelve la actividad demuestre criterio
        contable: al mirar la data tiene que darse cuenta de que ese asiento no
        cuadra (debe != haber) y plantearlo.

        Nota: el asiento descuadrado queda en un estado "sucio". Se ve bien en
        la vista, pero cualquier edicion/guardado vuelve a disparar
        ``_check_balanced`` y ahi si Odoo bloquea. Es esperado.
        """
        company = self.env.company
        Journal = self.env["account.journal"]
        Account = self.env["account.account"]

        journal = Journal.search(
            [*Journal._check_company_domain(company.id), ("type", "=", "general")],
            limit=1,
        )
        accounts = Account.search(
            [*Account._check_company_domain(company.id)],
            limit=2,
        )
        if not journal or len(accounts) < 2:
            _logger.warning(
                "real_state_management: no hay diario 'general' o plan de cuentas "
                "disponible; se omite la data contable de la actividad."
            )
            return

        account_a, account_b = accounts[0], accounts[1]
        today = fields.Date.context_today(self)

        # 1) Asiento correcto: debe == haber (1000 == 1000).
        correct = self.create(
            {
                "move_type": "entry",
                "journal_id": journal.id,
                "date": today,
                "ref": "Actividad",
                "line_ids": [
                    Command.create(
                        {
                            "account_id": account_a.id,
                            "name": "Debe",
                            "debit": 1000.0,
                            "credit": 0.0,
                        }
                    ),
                    Command.create(
                        {
                            "account_id": account_b.id,
                            "name": "Haber",
                            "debit": 0.0,
                            "credit": 1000.0,
                        }
                    ),
                ],
            }
        )
        correct.action_post()

        # 2) Asiento a revisar: se crea balanceado (1500 == 1500) para pasar la
        #    validacion del ORM, se postea, y recien despues se descuadra por SQL.
        unbalanced = self.create(
            {
                "move_type": "entry",
                "journal_id": journal.id,
                "date": today,
                "ref": "Actividad",
                "line_ids": [
                    Command.create(
                        {
                            "account_id": account_a.id,
                            "name": "Debe",
                            "debit": 1500.0,
                            "credit": 0.0,
                        }
                    ),
                    Command.create(
                        {
                            "account_id": account_b.id,
                            "name": "Haber",
                            "debit": 0.0,
                            "credit": 1500.0,
                        }
                    ),
                ],
            }
        )

        # Se postea mientras todavia cuadra (1500 == 1500): pasa _check_balanced.
        unbalanced.action_post()

        # Nos aseguramos de que las lineas esten persistidas antes del UPDATE crudo.
        self.env.flush_all()
        debit_line = unbalanced.line_ids.filtered(lambda line: line.debit)[:1]

        # Rompemos el balance: el debe pasa de 1500 a 1800 sin tocar el haber
        # (1500). Queda un descuadre de 300 que el ORM no dejaria guardar por
        # _check_balanced, pero que via SQL directo si persiste.
        self.env.cr.execute(
            """
            UPDATE account_move_line
               SET debit = debit + 300,
                   balance = balance + 300,
                   amount_currency = amount_currency + 300
             WHERE id = %s
            """,
            [debit_line.id],
        )

        # Invalidamos la cache para que el descuadre se refleje al leer el asiento.
        self.env.invalidate_all()

        # 3) Asiento de venta con IVA mal liquidado. A diferencia del anterior,
        #    este CUADRA (debe == haber == 1150), asi que pasa _check_balanced sin
        #    necesidad de tocarlo por SQL. La trampa es puramente contable: la base
        #    gravada es 1000 y el IVA declarado es 150 (15%), cuando al 21% deberia
        #    ser 210 (y el total factura, 1210). Quien resuelve la actividad tiene
        #    que notar que el IVA no se corresponde con la base imponible.
        def _account_of_type(account_type, fallback):
            acc = Account.search(
                [
                    *Account._check_company_domain(company.id),
                    ("account_type", "=", account_type),
                ],
                limit=1,
            )
            return acc or fallback

        receivable = _account_of_type("asset_receivable", account_a)
        income = _account_of_type("income", account_b)
        tax_account = _account_of_type("liability_current", account_a)

        iva_move = self.create(
            {
                "move_type": "entry",
                "journal_id": journal.id,
                "date": today,
                "ref": "Actividad",
                "line_ids": [
                    Command.create(
                        {
                            "account_id": receivable.id,
                            "name": "Cliente - total factura",
                            "debit": 1150.0,
                            "credit": 0.0,
                        }
                    ),
                    Command.create(
                        {
                            "account_id": income.id,
                            "name": "Ventas gravadas (base imponible)",
                            "debit": 0.0,
                            "credit": 1000.0,
                        }
                    ),
                    Command.create(
                        {
                            "account_id": tax_account.id,
                            "name": "IVA Debito Fiscal 21%",
                            "debit": 0.0,
                            "credit": 150.0,
                        }
                    ),
                ],
            }
        )
        iva_move.action_post()

        _logger.info(
            "real_state_management: data contable de la actividad creada "
            "(asiento %s descuadrado; ademas un asiento de venta con IVA mal "
            "liquidado).",
            unbalanced.id,
        )
