from fastapi import APIRouter, Depends
from app.schemas.user.user_schema import UserCreateSchema, UserLoginSchema
from app.services.user_service import UserService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", summary="Create a new user")
def create_user(user: UserCreateSchema):
    return UserService.create_user(user)


@router.post("/login", summary="Login")
def login(credentials: UserLoginSchema):
    return UserService.login(credentials)


@router.get("/me", summary="Get current logged user")
def get_me(current_user: dict = Depends(get_current_user)):
    current_user.pop("password", None)
    current_user["_id"] = str(current_user["_id"])
    return current_user