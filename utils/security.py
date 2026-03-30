from passlib.context import CryptContext

# 1. 创建密码上下文
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 2. 加密
def get_hash_password(password:str)->str :
    return pwd_context.hash(password)

# 3. 校验 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)