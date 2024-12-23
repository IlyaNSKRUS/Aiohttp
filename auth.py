from bcrypt import hashpw, checkpw, gensalt
from models import Session
from aiohttp import web, request


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    hashed_password_bytes = hashpw(password_bytes, gensalt())
    hashed_password = hashed_password_bytes.decode()
    return hashed_password

def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode()
    hashed_password_bytes = hashed_password.encode()
    return checkpw(password_bytes, hashed_password_bytes)


def check_token(handler):
    async def wrapper(*args, **kwargs):

        token = await request.session.json()

        # if token is None:
        #     raise
        # token = request.session.query(Token).filter_by(token=token).first()
        # if token is None:
        #     raise
        # request.token = token
        return handler(*args, **kwargs)

    return wrapper



