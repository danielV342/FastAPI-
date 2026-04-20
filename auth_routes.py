from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"jfnksfjbasbfkhbkbsdbfo{id_usuario}"
    return token

@auth_router.get("/")
async def auth():
    """
    Essa e a rota de autenticacao padrao do sistema
    """
    return {"mensagem": "Voce acessou a rota padrao de autenticacao", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario: 
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
        #já existe um usuário
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }