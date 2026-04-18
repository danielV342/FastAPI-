from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """
    Essa e a rota de autenticacao padrao do sistema
    """
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}