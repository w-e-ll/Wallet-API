from lib.models import Operation, Wallet
from lib.validation import OperationResponse, WalletResponse


def to_wallet_response(wallet: Wallet) -> WalletResponse:
    return WalletResponse(
        wallet_id=wallet.wallet_id,
        owner=wallet.owner,
        balance=f"{wallet.balance:.2f}",
        created_at=wallet.created_at
    )

def to_operation_response(operation: Operation) -> OperationResponse:
    return OperationResponse(
        operation_id=operation.operation_id,
        wallet_id=operation.wallet_id,
        idempotency_key=operation.idempotency_key,
        amount=f"{operation.amount:.2f}",
        operation_type=operation.operation_type,
        created_at=operation.created_at
    )