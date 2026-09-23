from app.database.mongodb import db


class MedicaoRepository:

    collection = db["medicoes"]

    @classmethod
    def create(cls, medicao_data: dict):
        result = cls.collection.insert_one(medicao_data)
        return str(result.inserted_id)

    @classmethod
    def find_all(cls, filters: dict, limit: int):
        cursor = cls.collection.find(filters).sort("timestamp", -1).limit(limit)
        return list(cursor)

    @classmethod
    def find_latest(cls, device_id: str = None):
        query = {"deviceId": device_id} if device_id else {}
        return cls.collection.find_one(query, sort=[("timestamp", -1)])

    @classmethod
    def find_volumes_by_device(cls, device_id: str):
        cursor = cls.collection.find(
            {"deviceId": device_id},
            {"volume": 1, "_id": 0}
        )
        return [doc["volume"] for doc in cursor if "volume" in doc]

    @classmethod
    def sum_volume_between(cls, device_id: str, start, end) -> float:
        cursor = cls.collection.find(
            {
                "deviceId": device_id,
                "timestamp": {"$gte": start, "$lt": end},
            },
            {"volume": 1, "_id": 0}
        )
        return sum(doc["volume"] for doc in cursor if "volume" in doc)

    @classmethod
    def find_volumes_since(cls, device_id: str, since):
        cursor = cls.collection.find(
            {
                "deviceId": device_id,
                "timestamp": {"$gte": since},
            },
            {"volume": 1, "timestamp": 1, "_id": 0}
        )
        return list(cursor)

    @classmethod
    def sum_volume_since(cls, device_id: str, since=None) -> float:
        query = {"deviceId": device_id}
        if since:
            query["timestamp"] = {"$gte": since}
        cursor = cls.collection.find(query, {"volume": 1, "_id": 0})
        return sum(doc["volume"] for doc in cursor if "volume" in doc)