from app.repositories.ciclo_custo_repository import CicloCustoRepository
from app.services.medicao_service import MedicaoService


class CustoService:

    @staticmethod
    def get_custo(device_id: str, user_email: str) -> dict:
        ciclo = CicloCustoRepository.find_by_user(user_email)
        inicio = ciclo["inicio"] if ciclo else None
        return MedicaoService.get_consumption_cost(device_id, inicio)

    @staticmethod
    def reiniciar_ciclo(device_id: str, user_email: str) -> dict:
        novo_inicio = CicloCustoRepository.reiniciar(user_email, device_id)
        return {"message": "Ciclo de custo reiniciado com sucesso", "cicloIniciadoEm": novo_inicio}