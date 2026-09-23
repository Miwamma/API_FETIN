from datetime import datetime
from fastapi import HTTPException
from app.repositories.conta_agua_repository import ContaAguaRepository
from app.schemas.conta_agua.conta_agua_schema import ContaAguaCreateSchema

QTD_CONTAS_PARA_REFERENCIA = 3


class ContaAguaService:

    @staticmethod
    def create_conta(user_email: str, conta: ContaAguaCreateSchema):
        conta_dict = conta.model_dump()
        conta_dict["userEmail"] = user_email
        conta_dict["createdAt"] = datetime.utcnow()

        conta_id = ContaAguaRepository.create(conta_dict)
        return {"message": "Conta de água registrada com sucesso", "id": conta_id}

    @staticmethod
    def _serialize(doc: dict) -> dict:
        doc["id"] = str(doc.pop("_id"))
        doc.pop("userEmail", None)
        return doc

    @staticmethod
    def list_contas(user_email: str, limit: int = None):
        docs = ContaAguaRepository.find_by_user(user_email, limit=limit)
        return [ContaAguaService._serialize(doc) for doc in docs]

    @staticmethod
    def delete_conta(user_email: str, conta_id: str):
        deletado = ContaAguaRepository.delete_by_id(conta_id, user_email)
        if not deletado:
            raise HTTPException(status_code=404, detail="Conta de água não encontrada")
        return {"message": "Conta de água removida com sucesso"}

    @staticmethod
    def get_daily_reference(user_email: str) -> dict:
        docs = ContaAguaRepository.find_by_user(user_email)

        if len(docs) < QTD_CONTAS_PARA_REFERENCIA:
            raise HTTPException(
                status_code=422,
                detail=f"É necessário cadastrar pelo menos {QTD_CONTAS_PARA_REFERENCIA} contas de água para calcular a referência (você tem {len(docs)})"
            )

        ultimas_contas = docs[:QTD_CONTAS_PARA_REFERENCIA]
        valores_m3 = [doc["consumoM3"] for doc in ultimas_contas if "consumoM3" in doc]

        media_m3 = sum(valores_m3) / len(valores_m3)
        referencia_diaria_m3 = media_m3 / 30

        return {
            "mediaM3": round(media_m3, 3),
            "referenciaDiariaM3": round(referencia_diaria_m3, 5),
            "referenciaDiariaLitros": round(referencia_diaria_m3 * 1000, 2),
            "quantidadeContasConsideradas": len(ultimas_contas),
            "quantidadeContasTotal": len(docs),
        }