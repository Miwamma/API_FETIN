from fastapi import APIRouter, Depends, Query
from app.schemas.conta_agua.conta_agua_schema import ContaAguaCreateSchema
from app.services.conta_agua_service import ContaAguaService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/contas-agua", tags=["Contas de Água"])


@router.post("", summary="Registrar uma conta de água anterior")
def create_conta(conta: ContaAguaCreateSchema, current_user: dict = Depends(get_current_user)):
    return ContaAguaService.create_conta(current_user["email"], conta)


@router.get("", summary="Listar contas de água cadastradas (mais recentes primeiro)")
def list_contas(limit: int = Query(default=5, ge=1, le=100), current_user: dict = Depends(get_current_user)):
    return ContaAguaService.list_contas(current_user["email"], limit)


@router.delete("/{conta_id}", summary="Remover uma conta de água cadastrada")
def delete_conta(conta_id: str, current_user: dict = Depends(get_current_user)):
    return ContaAguaService.delete_conta(current_user["email"], conta_id)


@router.get("/referencia-diaria", summary="Referência diária de consumo, calculada pela média das 3 contas mais recentes")
def get_daily_reference(current_user: dict = Depends(get_current_user)):
    return ContaAguaService.get_daily_reference(current_user["email"])