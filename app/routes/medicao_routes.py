import logging
from fastapi import APIRouter, Query, HTTPException, status, Depends
from datetime import datetime
from typing import Optional

from app.schemas.medicao.medicao_schema import MedicaoCreateSchema
from app.services.medicao_service import MedicaoService
from app.services.consumo_atipico_service import ConsumoAtipicoService
from app.repositories.user_repository import UserRepository
from app.core.dependencies import get_authenticated_device_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/medicoes", tags=["Medições"])


@router.post("", status_code=status.HTTP_201_CREATED, summary="Registrar uma nova medição do ESP32")
def create_medicao(medicao: MedicaoCreateSchema):
    dono = UserRepository.find_by_device_id(medicao.deviceId)
    if not dono:
        raise HTTPException(
            status_code=403, 
            detail="deviceId não está vinculado a nenhum usuário cadastrado"
        )

    resultado = MedicaoService.create_medicao(medicao)

    try:
        ConsumoAtipicoService.verificar_e_notificar(medicao.deviceId, dono)
    except Exception as exc:
        # Uma falha na notificação nunca pode derrubar o registro da medição em si
        logger.error(f"Falha ao verificar/notificar consumo atípico: {exc}")

    return resultado


@router.get("/latest", summary="Obter a medição mais recente")
def get_latest(device_id: str = Depends(get_authenticated_device_id)):
    result = MedicaoService.get_latest(device_id)
    if not result:
        raise HTTPException(status_code=404, detail="Nenhuma medição encontrada")
    return result


@router.get("/consumption", summary="Consumo total de água (litros)")
def get_total_consumption(device_id: str = Depends(get_authenticated_device_id)):
    return MedicaoService.get_total_consumption(device_id)


@router.get("/consumption/cubic-meters", summary="Consumo total em metros cúbicos")
def get_consumption_cubic_meters(device_id: str = Depends(get_authenticated_device_id)):
    return MedicaoService.get_consumption_cubic_meters(device_id)


@router.get("/consumption/cost", summary="Custo total estimado do consumo de água")
def get_consumption_cost(device_id: str = Depends(get_authenticated_device_id)):
    return MedicaoService.get_consumption_cost(device_id)


@router.get("", summary="Listar medições")
def list_medicoes(
    sensor_id: Optional[str] = Query(default=None, alias="sensorId"),
    inicio: Optional[datetime] = Query(default=None),
    fim: Optional[datetime] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    device_id: str = Depends(get_authenticated_device_id),
):

    return MedicaoService.list_medicoes(device_id, sensor_id, inicio, fim, limit)


@router.get("/analise", summary="Obter análise de consumo")
def obter_analise_consumo(device_id: str = Depends(get_authenticated_device_id)):

    return MedicaoService.analisar_consumo(device_id)