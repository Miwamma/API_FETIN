from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.medicao_routes import router as medicao_router
from app.routes.conta_agua_routes import router as conta_agua_router
from app.routes.consumo_atipico_routes import router as consumo_atipico_router
from app.routes.anomalia_routes import router as anomalia_router
from app.routes.notificacao_routes import router as notificacao_router
from app.routes.custo_routes import router as custo_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(medicao_router)
app.include_router(conta_agua_router)
app.include_router(consumo_atipico_router)
app.include_router(anomalia_router)
app.include_router(notificacao_router)
app.include_router(custo_router)

@app.get("/")
def home():
    return {"message": "API funcionando"}