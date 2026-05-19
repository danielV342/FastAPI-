from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verificar_token)])

def criar_token(id_usuario):
    token = f"klsdmfknsjfkjdh{id_usuario}"
    return token

@order_router.get("/")
async def pedidos():
    """
    Essa e a rota de pedidos padrao do sistema
    """
    return {"mensagem": "Voce acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema, 
    session: Session = Depends(pegar_sessao)
):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)

    session.add(novo_pedido)
    session.commit()

    return {"mensagem": f"Pedido criado com sucesso. ID do pedido {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends(verificar_token)
):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação.")

    pedido.status = "CANCELADO"
    session.commit()

    return {
        "mensagem": f"Pedido {pedido.id} cancelado com sucesso.",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(
    session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends(verificar_token)
):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer esta operação.")
    
    else: 
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
    
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(
    id_pedido: int,
    item_pedido_schema: ItemPedidoSchema, 
    session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends(verificar_token)
):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente.")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    
    item_pedido = ItemPedido(
    quantidade=item_pedido_schema.quantidade,
    sabor=item_pedido_schema.sabor,
    tamanho=item_pedido_schema.tamanho,
    preco_unitario=item_pedido_schema.preco_unitario,
    pedido=id_pedido
)
    
    session.add(item_pedido)
    session.flush() 
    pedido.calcular_preco()
    session.commit()

    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(
    id_item_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item não existente.")
    
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação.")
    
    session.delete(item_pedido)
    session.flush()           
    pedido.calcular_preco() 

    return {
        "mensagem": "Item removido com sucesso",
        "preco_pedido": pedido.preco
    }