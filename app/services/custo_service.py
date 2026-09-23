from fastapi import HTTPException
from app.repositories.ciclo_custo_repository import CicloCustoRepository
from app.repositories.medicao_repository import MedicaoRepository
from app.core import config


class CustoService:

    @staticmethod
    def get_custo(device_id: str, user_email: str) -> dict:
        ciclo = CicloCustoRepository.find_by_user(user_email)
        inicio = ciclo["inicio"] if ciclo else None

        litros = MedicaoRepository.sum_volume_since(device_id, inicio)
        m3 = litros / 1000

        tariff = config.WATER_TARIFF_PER_CUBIC_METER
        if tariff is None or tariff < 0:
            raise HTTPException(status_code=500, detail="Tarifa de água configurada com valor inválido")

        return {
            "deviceId": device_id,
            "totalLiters": round(litros, 3),
            "totalCubicMeters": round(m3, 5),
            "waterTariffPerCubicMeter": tariff,
            "totalCost": round(m3 * tariff, 2),
            "cicloIniciadoEm": inicio,
        }

    @staticmethod
    def reiniciar_ciclo(device_id: str, user_email: str) -> dict:
        novo_inicio = CicloCustoRepository.reiniciar(user_email, device_id)
        return {"message": "Ciclo de custo reiniciado com sucesso", "cicloIniciadoEm": novo_inicio}