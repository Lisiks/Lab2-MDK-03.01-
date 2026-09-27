from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password):
    return context.hash(plain_password)

def verify_password(plaint_password, hash_password):
    return context.verify(plaint_password, hash_password)