from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str) -> str:
    "Hashing password"
    return pwd_context.hash(password)


def verify_pwd(plain_pwd: str, hashed_pwd: str):
    "Vetifying provided password"
    return pwd_context.verify(plain_pwd, hashed_pwd)
