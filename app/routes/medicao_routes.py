from fastapi import APIRouter, Query, HTTPException, status, Depends
from datetime import datetime
from typing import Optional
from app.schemas.medicao.medicao_schema import MedicaoCreateSchema
from app.services.medicao_service import MedicaoService
from app.services.consumo_atipico_service import ConsumoAtipicoService
from app.repositories.user_repository import UserRepository
from app.repositories.ciclo_custo_repository import CicloCustoRepository
from app.core.dependencies import get_authenticated_device_id, get_current_user

router = APIRouter(prefix="/medicoes", tags=["Medições"])


def _obter_inicio_ciclo(user_email: str):
    ciclo = CicloCustoRepository.find_by_user(user_email)
    return ciclo["inicio"] if ciclo else None


@router.post("", status_code=status.HTTP_201_CREATED, summary="Registrar uma nova medição do ESP32")
def create_medicao(medicao: MedicaoCreateSchema):
    dono = UserRepository.find_by_device_id(medicao.deviceId)
    if not dono:
        raise HTTPException(status_code=403, detail="deviceId não está vinculado a nenhum usuário cadastrado")

    resultado = MedicaoService.create_medicao(medicao)

    try:
        ConsumoAtipicoService.verificar_e_notificar(medicao.deviceId, dono)
    except Exception as exc:
        print(f"Falha ao verificar/notificar consumo atípico: {exc}")

    return resultado


@router.get("/latest", summary="Obter a medição mais recente")
def get_latest(device_id: str = Depends(get_authenticated_device_id)):
    result = MedicaoService.get_latest(device_id)
    if not result:
        raise HTTPException(status_code=404, detail="Nenhuma medição encontrada")
    return result


@router.get("/consumption", summary="Consumo total de água (litros) desde o último reinício de ciclo")
def get_total_consumption(
    device_id: str = Depends(get_authenticated_device_id),
    current_user: dict = Depends(get_current_user),
):
    since = _obter_inicio_ciclo(current_user["email"])
    return MedicaoService.get_total_consumption(device_id, since)


@router.get("/consumption/cubic-meters", summary="Consumo total em metros cúbicos desde o último reinício de ciclo")
def get_consumption_cubic_meters(
    device_id: str = Depends(get_authenticated_device_id),
    current_user: dict = Depends(get_current_user),
):
    since = _obter_inicio_ciclo(current_user["email"])
    return MedicaoService.get_consumption_cubic_meters(device_id, since)


@router.get("/consumption/cost", summary="Custo total estimado desde o último reinício de ciclo")
def get_consumption_cost(
    device_id: str = Depends(get_authenticated_device_id),
    current_user: dict = Depends(get_current_user),
):
    since = _obter_inicio_ciclo(current_user["email"])
    return MedicaoService.get_consumption_cost(device_id, since)


@router.get("", summary="Listar medições")
def list_medicoes(
    sensorId: Optional[str] = Query(default=None),
    inicio: Optional[datetime] = Query(default=None),
    fim: Optional[datetime] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    device_id: str = Depends(get_authenticated_device_id),
):
    return MedicaoService.list_medicoes(device_id, sensorId, inicio, fim, limit)