from fastapi import APIRouter, Depends
from app.services.custo_service import CustoService
from app.core.dependencies import get_current_user, get_authenticated_device_id

router = APIRouter(prefix="/custo", tags=["Custo"])


@router.get("", summary="Custo estimado do ciclo atual")
def get_custo(
    device_id: str = Depends(get_authenticated_device_id),
    current_user: dict = Depends(get_current_user),
):
    return CustoService.get_custo(device_id, current_user["email"])


@router.post("/reiniciar", summary="Reiniciar o ciclo de custo (descarta o consumo acumulado, sem apagar as medições)")
def reiniciar_ciclo(
    device_id: str = Depends(get_authenticated_device_id),
    current_user: dict = Depends(get_current_user),
):
    return CustoService.reiniciar_ciclo(device_id, current_user["email"])