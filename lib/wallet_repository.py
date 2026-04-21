from typing import Optional, List, Dict
from lib.models import Wallet, Operation


class InMemoryWalletRepository:
    def __init__(self) -> None:
        self._wallets: Dict[str, Wallet] = {}

    def create(self, wallet: Wallet) -> Wallet:
        if wallet.wallet_id not in self._wallets:
            self._wallets[wallet.wallet_id] = wallet
        return wallet

    def get(self, wallet_id: str) -> Optional[Wallet]:
        return self._wallets.get(wallet_id)

    def list_operations(self, wallet_id: str) -> List[Operation]:
        wallet = self._wallets.get(wallet_id)
        if not wallet:
            raise KeyError("Wallet not found")

        return wallet.operations


class InMemoryIdempotencyRepository:
    def __init__(self) -> None:
        self._processed: Dict[tuple[str, str], Operation] = {}

    def get(self, wallet_id: str, idempotency_key: str) -> Optional[Operation]:
        if not wallet_id:
            raise KeyError("Wallet_id required")
        if not idempotency_key:
            raise KeyError("Idempotency_key required")
        if wallet_id and idempotency_key:
            return self._processed.get((wallet_id, idempotency_key))
        else:
            raise KeyError(f"{wallet_id}, {idempotency_key}")

    def save(self, wallet_id: str, idempotency_key: str, operation: Operation) -> None:
        if not wallet_id:
            raise KeyError("Wallet_if required")
        if not idempotency_key:
            raise KeyError("Idempotency_key required")
        if not isinstance(operation, Operation):
            raise KeyError("Operation required")
        self._processed[(wallet_id, idempotency_key)] = operation
        return
