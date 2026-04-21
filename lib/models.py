from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import List

from decimal import Decimal

from lib.types import OperationType

@dataclass
class Operation:
    operation_id: str
    wallet_id: str
    operation_type: OperationType
    amount: Decimal
    created_at: datetime
    idempotency_key: str


@dataclass
class Wallet:
    wallet_id: str
    owner: str
    balance: Decimal = Decimal("0.00")
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    operations: List[Operation] = field(default_factory=list)
