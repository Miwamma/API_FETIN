from fastapi import APIRouter, Query, HTTPException, status
from datetime import datetime
from typing import Optional
from app.schemas.medicao.medicao_schema import MedicaoCreateSchema
from app.services.medicao_service import MedicaoService

router = APIRouter(prefix="/medicoes", tags=["Medições"])


@router.post("", status_code=status.HTTP_201_CREATED, summary="Registrar uma nova medição do ESP32")
def create_medicao(medicao: MedicaoCreateSchema):
    return MedicaoService.create_medicao(medicao)


@router.get("/latest", summary="Obter a medição mais recente")
def get_latest(deviceId: Optional[str] = Query(default=None)):
    result = MedicaoService.get_latest(deviceId)
    if not result:
        raise HTTPException(status_code=404, detail="Nenhuma medição encontrada")
    return result


@router.get("/consumption/{deviceId}", summary="Consumo total de água (litros)")
def get_total_consumption(deviceId: str):
    return MedicaoService.get_total_consumption(deviceId)


@router.get("/consumption/{deviceId}/cubic-meters", summary="Consumo total em metros cúbicos")
def get_consumption_cubic_meters(deviceId: str):
    return MedicaoService.get_consumption_cubic_meters(deviceId)


@router.get("/consumption/{deviceId}/cost", summary="Custo total estimado do consumo de água")
def get_consumption_cost(deviceId: str):
    return MedicaoService.get_consumption_cost(deviceId)


@router.get("", summary="Listar medições")
def list_medicoes(
    deviceId: Optional[str] = Query(default=None),
    sensorId: Optional[str] = Query(default=None),
    inicio: Optional[datetime] = Query(default=None),
    fim: Optional[datetime] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
):
    return MedicaoService.list_medicoes(deviceId, sensorId, inicio, fim, limit)

@router.get("/analise/{device_id}")
def obter_analise_consumo(device_id: str):
    return MedicaoService.analisar_consumo(device_id)
    