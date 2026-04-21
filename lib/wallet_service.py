from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from threading import RLock
from typing import List
from uuid import uuid4

from fastapi import HTTPException, status

from lib.models import Operation, Wallet
from lib.wallet_repository import InMemoryWalletRepository, InMemoryIdempotencyRepository


class WalletService:
    def __init__(
            self,
            wallet_repository: InMemoryWalletRepository,
            idempotency_repository: InMemoryIdempotencyRepository
    ) -> None:
        self._wallet_repository = wallet_repository
        self._idempotency_repository = idempotency_repository
        self._lock = RLock()

    def create_wallet(self, owner: str) -> Wallet:
        wallet = Wallet(owner=owner.strip(), wallet_id=str(uuid4()))
        return self._wallet_repository.create(wallet)

    def get_wallet(self, wallet_id: str) -> Wallet:
        wallet = self._wallet_repository.get(wallet_id)
        if wallet is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wallet {wallet_id} not found")
        return wallet

    def list_operations(self, wallet_id: str) -> List[Operation]:
        wallet = self.get_wallet(wallet_id)
        return wallet.operations

    def deposit(self, wallet_id: str, raw_amount: str, idempotency_key: str) -> Operation:
        try:
            amount = Decimal(raw_amount).quantize(Decimal("0.01"))
        except InvalidOperation as exc:
            raise ValueError("Amount must be a number") from exc

        with self._lock:
            existing_operation = self._idempotency_repository.get(wallet_id, idempotency_key)
            if existing_operation:
                if existing_operation.amount != amount:
                    raise HTTPException(409, "Idempotency key conflict")
                return existing_operation

            wallet = self.get_wallet(wallet_id)

            wallet.balance += amount

            operation = Operation(
                operation_id=str(uuid4()),
                wallet_id=wallet_id,
                idempotency_key=idempotency_key,
                amount=amount,
                created_at=datetime.now(timezone.utc),
                operation_type="deposit",
            )

            wallet.operations.append(operation)
            self._idempotency_repository.save(wallet_id, idempotency_key, operation)
            return operation

    def withdraw(self, wallet_id: str, idempotency_key: str, raw_amount: str) -> Operation:
        amount = Decimal(raw_amount).quantize(Decimal("0.01"))

        with self._lock:
            existing_operation = self._idempotency_repository.get(wallet_id, idempotency_key)
            if existing_operation:
                if existing_operation.amount != amount:
                    raise HTTPException(409, "Idempotency key conflict")
                return existing_operation

            wallet = self.get_wallet(wallet_id)

            if wallet.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Insufficient funds"
                )

            wallet.balance -= amount

            operation = Operation(
                operation_id=str(uuid4()),
                wallet_id=wallet_id,
                operation_type="withdraw",
                amount=amount,
                created_at=datetime.now(timezone.utc),
                idempotency_key=idempotency_key
            )

            wallet.operations.append(operation)
            self._idempotency_repository.save(wallet_id, idempotency_key, operation)
            return operation
