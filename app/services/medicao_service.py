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
    def get_total_consumption(device_id: str) -> dict:
        volumes = MedicaoRepository.find_volumes_by_device(device_id)

        if not volumes:
            raise HTTPException(
                status_code=404,
                detail=f"Nenhuma medição encontrada para o deviceId '{device_id}'"
            )

        valid_volumes = [v for v in volumes if isinstance(v, (int, float)) and v >= 0]

        if not valid_volumes:
            raise HTTPException(
                status_code=422,
                detail=f"Medições encontradas para '{device_id}', mas nenhuma possui volume válido"
            )

        total_liters = sum(valid_volumes)

        return {
            "deviceId": device_id,
            "totalLiters": round(total_liters, 3),
        }

    @staticmethod
    def get_consumption_cubic_meters(device_id: str) -> dict:
        result = MedicaoService.get_total_consumption(device_id)
        result["totalCubicMeters"] = round(result["totalLiters"] / 1000, 5)
        return result

    @staticmethod
    def get_consumption_cost(device_id: str) -> dict:
        result = MedicaoService.get_consumption_cubic_meters(device_id)

        tariff = config.WATER_TARIFF_PER_CUBIC_METER
        if tariff is None or tariff < 0:
            raise HTTPException(
                status_code=500,
                detail="Tarifa de água (WATER_TARIFF_PER_CUBIC_METER) está configurada com valor inválido"
            )

        result["waterTariffPerCubicMeter"] = tariff
        result["totalCost"] = round(result["totalCubicMeters"] * tariff, 2)
        return result


        from app.repositories.medicao_repository import MedicaoRepository

class MedicaoService:
   

    @staticmethod
    def analisar_consumo(device_id: str):
        # Busca as ultimas 15 medicoes
        medicoes = MedicaoRepository.find_all({"deviceId": device_id}, limit=15)

        if not medicoes or len(medicoes) < 2:
            return {
                "device_id": device_id,
                "consumo_atual": medicoes[0].get("volume", 0) if medicoes else 0,
                "media_consumo": 0,
                "alerta_atipico": False,
                "mensagem": "Histórico insuficiente."
            }

        consumo_atual = medicoes[0].get("volume", 0)
        volumes_anteriores = [m.get("volume", 0) for m in medicoes[1:] if "volume" in m]
        
        media = sum(volumes_anteriores) / len(volumes_anteriores)
        limite_aceitavel = media * 1.3 # 30% acima da media
        is_atipico = consumo_atual > limite_aceitavel

        return {
            "device_id": device_id,
            "consumo_atual": round(consumo_atual, 2),
            "media_consumo": round(media, 2),
            "limite_aceitavel": round(limite_aceitavel, 2),
            "alerta_atipico": is_atipico,
            "mensagem": " Alerta: Consumo acima do normal detectado!" if is_atipico else " Consumo dentro da normalidade."
        }