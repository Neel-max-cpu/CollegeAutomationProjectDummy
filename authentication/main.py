from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWSError, jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient

SECRET_KEY = "b7f8a0d3e1c529764f2e73cb9a68dc05"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client['test']
collection = db['emp_db']

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    employeeId: int or None = None

class User(BaseModel):
    employeeId: int
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None
    password:str

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(employeeId: int):
    user_data = await collection.find_one({"employeeId": employeeId})
    if user_data:
        return UserInDB(**user_data)
    else:
        return {"error": "Employee not found"}

async def create_user(user: UserInDB):
    user_dict = user.dict()
    user_dict['hashed_password'] = get_password_hash(user_dict['password'])
    del user_dict['password']
    await collection.insert_one(user_dict)
    return user

async def authenticate_user(employeeId: int, password: str):
    user = await get_user(employeeId)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not authenticate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        employeeId: str = payload.get("sub")
        if employeeId is None:
            raise credential_exception
        token_data = TokenData(employeeId=employeeId)
    except JWSError:
        raise credential_exception
    
    user = await get_user(token_data.employeeId)
    if not user:
        raise credential_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(int(form_data.username), form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect ID or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.employeeId}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/users/me', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get('/users/me/items')
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

@app.post('/users/', response_model=User)
async def create_user_route(user: UserInDB):
    user.hashed_password=get_password_hash(user.hashed_password)
    created_user = await create_user(user)
    return {'200':'User Successfully created'}
