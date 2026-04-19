from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """
    Essa e a rota de autenticacao padrao do sistema
    """
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(nome: str, email: str, senha: str, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        return {"mensagem": "Já existe um usuário com este nome"}
        #já existe um usuário
    else:
        senha_criptografada = bcrypt_context.hash(senha[:72])
        novo_usuario = Usuario(nome, email, senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuário cadastrado com sucesso"}