from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os

from src.server.logs.index import Logger

logger = Logger('AUTH')
SECRET = os.environ.get('SECRET')
AUDIENCE = os.environ.get('AUDIENCE')
ISSUER = os.environ.get('ISSUER')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        if not token:
            raise HTTPException(status_code=401, detail="No access token found")

        logger.info(f'GETTING CURRENT USER: {token}')
        
        payload = jwt.decode(
            token, 
            SECRET, 
            algorithms=["HS256"], 
            audience=AUDIENCE
        )
        user_id = payload.get("sub")

        if user_id is None:
            logger.error('USER ID IS NONE')
            raise HTTPException(status_code=401, detail="Invalid token")
        
        logger.info(f'CURRENT USER: {user_id}')
        return payload.get("email")

    except ExpiredSignatureError:
        logger.error('EXPIRED TOKEN')
        raise HTTPException(status_code=401, detail="Token has expired")

    except JWTError:
        logger.error('INVALID AUDIENCE')
        raise HTTPException(status_code=401, detail="Invalid audience")

    except Exception as e:
        logger.error(f'GENERAL EXCEPTION: {e}')
        raise HTTPException(status_code=500, detail=str(e))
