from app.models.transaction import Transaction
import uuid

def create_or_get_transaction(db, user_id: str, amount: int):
    txn = Transaction(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=amount,
        status="PENDING"
    )

    db.add(txn)
    db.commit()
    db.refresh(txn)

    return txn
