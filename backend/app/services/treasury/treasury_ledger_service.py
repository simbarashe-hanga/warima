from decimal import Decimal

from sqlalchemy import func

from app.models.enums import WalletLedgerEntryType
from app.models.treasury_ledger import TreasuryLedger
from app.models.wallet_transaction import WalletTransaction


class TreasuryLedgerService:

    @staticmethod
    def _validate_treasury(treasury):
        if treasury is None:
            raise ValueError("Treasury is required")

    @staticmethod
    def _validate_amount(amount):
        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        return amount

    # --------------------------------------------------------------
    # TRANSACTION-BASED TREASURY ENTRIES
    # --------------------------------------------------------------

    @staticmethod
    def record_credit(
        db,
        treasury,
        amount,
        transaction_id,
    ):
        """
        Record a treasury CREDIT originating from a wallet transaction.

        Used by:
            Member contribution -> Stokvel treasury
        """

        TreasuryLedgerService._validate_treasury(treasury)

        if transaction_id is None:
            raise ValueError("Transaction ID is required")

        amount = TreasuryLedgerService._validate_amount(amount)

        transaction = (
            db.query(WalletTransaction)
            .filter(WalletTransaction.id == transaction_id)
            .one_or_none()
        )

        if transaction is None:
            raise ValueError("Wallet transaction not found")

        if transaction.currency != treasury.denomination.value:
            raise ValueError(
                f"Transaction currency {transaction.currency} "
                f"does not match treasury denomination "
                f"{treasury.denomination.value}"
            )

        entry = TreasuryLedger(
            treasury_id=treasury.id,
            transaction_id=transaction_id,
            investment_id=None,
            entry_type=WalletLedgerEntryType.CREDIT,
            amount=amount,
            currency=transaction.currency,
        )

        db.add(entry)
        db.flush()

        return entry

    @staticmethod
    def record_debit(
        db,
        treasury,
        amount,
        transaction_id,
    ):
        """
        Record a treasury DEBIT originating from a wallet transaction.

        Used for transaction-based treasury outflows.
        """

        TreasuryLedgerService._validate_treasury(treasury)

        if transaction_id is None:
            raise ValueError("Transaction ID is required")

        amount = TreasuryLedgerService._validate_amount(amount)

        entry = TreasuryLedger(
            treasury_id=treasury.id,
            transaction_id=transaction_id,
            investment_id=None,
            entry_type=WalletLedgerEntryType.DEBIT,
            amount=amount,
            currency=treasury.denomination.value,
        )

        db.add(entry)
        db.flush()

        return entry

    # --------------------------------------------------------------
    # INVESTMENT-BASED TREASURY ENTRIES
    # --------------------------------------------------------------

    @staticmethod
    def record_investment_debit(
        db,
        treasury,
        amount,
        investment_id,
    ):
        """
        Record treasury funds deployed into a collective investment.

        Accounting:

            Stokvel Treasury
                DEBIT
                -> StokvelInvestment
        """

        TreasuryLedgerService._validate_treasury(treasury)

        if investment_id is None:
            raise ValueError("Investment ID is required")

        amount = TreasuryLedgerService._validate_amount(amount)

        entry = TreasuryLedger(
            treasury_id=treasury.id,
            transaction_id=None,
            investment_id=investment_id,
            entry_type=WalletLedgerEntryType.DEBIT,
            amount=amount,
            currency=treasury.denomination.value,
        )

        db.add(entry)
        db.flush()

        return entry

    @staticmethod
    def record_investment_credit(
        db,
        treasury,
        amount,
        investment_id,
    ):
        """
        Record investment proceeds returning to the stokvel treasury.

        Accounting:

            StokvelInvestment
                CREDIT
                -> Stokvel Treasury
        """

        TreasuryLedgerService._validate_treasury(treasury)

        if investment_id is None:
            raise ValueError("Investment ID is required")

        amount = TreasuryLedgerService._validate_amount(amount)

        entry = TreasuryLedger(
            treasury_id=treasury.id,
            transaction_id=None,
            investment_id=investment_id,
            entry_type=WalletLedgerEntryType.CREDIT,
            amount=amount,
            currency=treasury.denomination.value,
        )

        db.add(entry)
        db.flush()

        return entry

    # --------------------------------------------------------------
    # TREASURY BALANCE
    # --------------------------------------------------------------

    @staticmethod
    def get_balance(
        db,
        treasury,
    ) -> Decimal:
        """
        Calculate the current treasury balance from the ledger.

        Balance:

            total CREDIT
            -
            total DEBIT

        The treasury ledger remains the source of truth.
        """

        TreasuryLedgerService._validate_treasury(treasury)

        treasury_currency = treasury.denomination.value

        credit = (
            db.query(func.coalesce(func.sum(TreasuryLedger.amount), 0))
            .filter(
                TreasuryLedger.treasury_id == treasury.id,
                TreasuryLedger.entry_type == WalletLedgerEntryType.CREDIT,
                TreasuryLedger.currency == treasury_currency,
            )
            .scalar()
        )

        debit = (
            db.query(func.coalesce(func.sum(TreasuryLedger.amount), 0))
            .filter(
                TreasuryLedger.treasury_id == treasury.id,
                TreasuryLedger.entry_type == WalletLedgerEntryType.DEBIT,
                TreasuryLedger.currency == treasury_currency,
            )
            .scalar()
        )

        return Decimal(str(credit)) - Decimal(str(debit))
