from models import db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from models import db, Usuario
from config import SECRET_KEY, ALGORITHM
from security import oauth2_schema

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close( )

def verificar_token(
    token: str = Depends(oauth2_schema), 
    session: Session = Depends(pegar_sessao)
):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dic_info.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()

    if not usuario: 
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    
    return usuario