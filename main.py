from __future__ import annotations
from typing import Literal

from fastapi import FastAPI, HTTPException, Path, status

from lib.models import Operation, Wallet
from lib.validation import OperationRequest, OperationResponse, WalletResponse, ErrorResponse, CreateWalletRequest, TransferRequest
from lib.wallet_repository import InMemoryWalletRepository, InMemoryIdempotencyRepository
from lib.wallet_service import WalletService
from lib.response_object import to_wallet_response, to_operation_response

app = FastAPI(title="Wallet API", version="1.0.0")

wallet_repository = InMemoryWalletRepository()
idempotency_repository = InMemoryIdempotencyRepository()
wallet_service = WalletService(wallet_repository, idempotency_repository)

@app.post(
    "/wallets",
    response_model=WalletResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}},
)
def create_wallet(payload: CreateWalletRequest) -> WalletResponse:
    owner = payload.owner.strip()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner must not be empty"
        )
    wallet = wallet_service.create_wallet(owner)
    return to_wallet_response(wallet)

@app.get(
    "/wallets/{wallet_id}",
    response_model=WalletResponse,
    responses={404: {"model": ErrorResponse}}
)
def get_wallet(wallet_id: str = Path(min_length=1)) -> WalletResponse:
    wallet = wallet_service.get_wallet(wallet_id)
    return to_wallet_response(wallet)


@app.post(
    "/wallets/{wallet_id}/deposit",
    response_model=OperationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": ErrorResponse}},
)
def deposit(wallet_id: str, payload: OperationRequest) -> OperationResponse:
    operation = wallet_service.deposit(
        wallet_id=wallet_id,
        raw_amount=payload.amount,
        idempotency_key=payload.idempotency_key,
    )
    return to_operation_response(operation)


@app.post(
    "/wallets/{wallet_id}/withdraw",
    response_model=OperationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def withdraw(wallet_id: str, payload: OperationRequest) -> OperationResponse:
    operation = wallet_service.withdraw(
        wallet_id=wallet_id,
        raw_amount=payload.amount,
        idempotency_key=payload.idempotency_key,
    )
    return to_operation_response(operation)


@app.get(
    "/wallets/{wallet_id}/operations",
    response_model=list[OperationResponse],
    responses={404: {"model": ErrorResponse}},
)
def list_operation(wallet_id: str) -> list[OperationResponse]:
    operations = wallet_service.list_operations(wallet_id)
    return [to_operation_response(operation) for operation in operations]


@app.post(
    "/wallets/transfer",
    response_model=OperationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def transfer(payload: TransferRequest) -> OperationResponse:
    operation = wallet_service.transfer(payload)
    return to_operation_response(operation)
