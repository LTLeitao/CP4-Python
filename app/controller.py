import sqlite3
from fastapi import APIRouter, HTTPException, status, Response
from app.schemas import UserCreate, UserUpdate
import app.services as services

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.get("/plans")
def list_plans():
    return services.list_plans()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        return services.create_user(user.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou CPF já cadastrado, ou ID do plano inválido."
        )

@router.get("")
def list_users():
    return services.list_users()

@router.get("/{user_id}")
def search_user(user_id: int):
    user = services.search_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado."
        )
    return user

@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    try:
        data = user.model_dump(exclude_unset=True)
        user_updated = services.update_user(user_id, data)
        if not user_updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Usuário não encontrado."
            )
        return user_updated
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou CPF já cadastrado em outro usuário, ou ID do plano inválido."
        )

@router.patch("/{user_id}")
def patch_user(user_id: int, user_data: UserUpdate):
    update_data = user_data.model_dump(exclude_unset=True)
    updated_user = services.patch_user(user_id, update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado."
        )
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    sucesso = services.delete_user(user_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)