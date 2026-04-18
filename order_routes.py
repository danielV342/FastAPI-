from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def pedidos():
    """
    Essa e a rota de pedidos padrao do sistema
    """
    return {"mensagem": "Voce acessou a rota de pedidos"}