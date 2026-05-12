from models import db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from models import db, Usuario
from config import SECRET_KEY, ALGORITHM



def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close( )

#esquema de autenticacao
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verificar_token(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(pegar_sessao)
): 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = payload.get("sub")

        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        usuario = session.query(Usuario).filter(usuario.id == int(id_usuario)).first()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return usuario
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
