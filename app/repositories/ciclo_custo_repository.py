from datetime import datetime
from app.database.mongodb import db


class CicloCustoRepository:

    collection = db["ciclos_custo"]

    @classmethod
    def find_by_user(cls, user_email: str):
        return cls.collection.find_one({"userEmail": user_email})

    @classmethod
    def reiniciar(cls, user_email: str, device_id: str):
        agora = datetime.utcnow()
        cls.collection.update_one(
            {"userEmail": user_email},
            {"$set": {"userEmail": user_email, "deviceId": device_id, "inicio": agora}},
            upsert=True
        )
        return agora