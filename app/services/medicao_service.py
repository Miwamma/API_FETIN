from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from app.repositories.medicao_repository import MedicaoRepository
from app.schemas.medicao.medicao_schema import MedicaoCreateSchema
from app.core import config


class MedicaoService:

    @staticmethod
    def create_medicao(medicao: MedicaoCreateSchema):
        medicao_dict = medicao.model_dump()
        medicao_dict["timestamp"] = datetime.utcnow()

        medicao_id = MedicaoRepository.create(medicao_dict)

        return {"message": "Medição registrada com sucesso", "id": medicao_id}

    @staticmethod
    def _serialize(doc: dict) -> dict:
        doc["id"] = str(doc.pop("_id"))
        return doc

    @staticmethod
    def list_medicoes(
        device_id: Optional[str] = None,
        sensor_id: Optional[str] = None,
        inicio: Optional[datetime] = None,
        fim: Optional[datetime] = None,
        limit: int = 100,
    ):
        filters = {}
        if device_id:
            filters["deviceId"] = device_id
        if sensor_id:
            filters["sensorId"] = sensor_id
        if inicio or fim:
            filters["timestamp"] = {}
            if inicio:
                filters["timestamp"]["$gte"] = inicio
            if fim:
                filters["timestamp"]["$lte"] = fim

        docs = MedicaoRepository.find_all(filters, limit)
        return [MedicaoService._serialize(doc) for doc in docs]

    @staticmethod
    def get_latest(device_id: Optional[str] = None):
        doc = MedicaoRepository.find_latest(device_id)
        if not doc:
            return None
        return MedicaoService._serialize(doc)

    @staticmethod
    def get_total_consumption(device_id: str, since=None) -> dict:
        total_liters = MedicaoRepository.sum_volume_since(device_id, since)

        return {
            "deviceId": device_id,
            "totalLiters": round(total_liters, 3),
            "cicloIniciadoEm": since,
        }

    @staticmethod
    def get_consumption_cubic_meters(device_id: str, since=None) -> dict:
        result = MedicaoService.get_total_consumption(device_id, since)
        result["totalCubicMeters"] = round(result["totalLiters"] / 1000, 5)
        return result

    @staticmethod
    def get_consumption_cost(device_id: str, since=None) -> dict:
        result = MedicaoService.get_consumption_cubic_meters(device_id, since)

        tariff = config.WATER_TARIFF_PER_CUBIC_METER
        if tariff is None or tariff < 0:
            raise HTTPException(status_code=500, detail="Tarifa de água configurada com valor inválido")

        result["waterTariffPerCubicMeter"] = tariff
        result["totalCost"] = round(result["totalCubicMeters"] * tariff, 2)
        return result