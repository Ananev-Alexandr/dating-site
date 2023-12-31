from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    eq_pass = pwd_context.verify(plain_password, hashed_password)
    return eq_pass


def get_password_hash(password) -> str:
    hash = pwd_context.hash(password)
    return hash
