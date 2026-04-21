from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from decimal import Decimal, InvalidOperation

from lib.types import OperationType

class CreateWalletRequest(BaseModel):
    owner: str = Field(min_length=1, max_length=100)


class WalletResponse(BaseModel):
    model_config: str = ConfigDict(from_attributes=True)

    wallet_id: str
    owner: str
    balance: str
    created_at: datetime


class OperationRequest(BaseModel):
    amount: str = Field(description="Amount of operation")
    idempotency_key: str = Field(min_length=1, max_length=100)

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: str) -> str:
        try:
            amount = Decimal(value)
        except InvalidOperation:
            raise ValueError("Amount must be a number")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        if amount.as_tuple().exponent < -2:
            raise ValueError("Too many decimal places")

        return value

class OperationResponse(BaseModel):
    operation_id: str
    wallet_id: str
    operation_type: OperationType
    amount: str
    created_at: datetime
    idempotency_key: str


class ErrorResponse(BaseModel):
    detail: str
