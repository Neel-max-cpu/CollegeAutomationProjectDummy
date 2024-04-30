from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import pymongo
import requests

# Initialize FastAPI app
app = FastAPI()

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users_collection = db["users"]

# JWT Settings
SECRET_KEY = "your_secret_key_is_hehe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class User(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    email: str
    # password: str  # Assuming you want to include the password in the class
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str



    

def get_user(email: str):
    user_data = users_collection.find_one({"email": email})
    if user_data:
        gmail = user_data.get("email")
        password = user_data.get("password")
        hashed_password = user_data.get("hashed_password")
        # print("User data found:", user_data)
        # print("Email:", gmail)
        # print("Password:", password)
        # print("Hashed Password:", hashed_password)
        if hashed_password:
            return UserInDB(email=gmail, hashed_password=hashed_password)            
    return None

    
    


# check if already present in the data base
def get_user_check(email: str):
    return users_collection.find_one({"email": email})


# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    # if (plain_password == hashed_password):
        # return 1
    # else: return 0



@app.post("/login", response_model=Token)   
async def login(user: User):
    db_user = get_user(user.email)
    print("DB User:", db_user)
    print("Provided Email:", user.email)
    if db_user:
        pass
    else:
        raise HTTPException(status_code=404, detail="User not registered")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}    

# Account Creation Endpoint
@app.post("/register")
async def register(user: User):
    existing_user = get_user_check(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    hashed_password = pwd_context.hash(user.password)
    # hashed_password = user.password
    user_data = {"email": user.email, "hashed_password": hashed_password}
    users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}


# Example protected route (requires authentication)
@app.get("/protected")
async def protected_route():
    return {"message": "This is a protected route"}

