



# # create table and enter data manually

# from sqlalchemy import create_engine, MetaData, Table, Column, Integer,Text, String, insert

# # Define your connection parameters
# username = "neel"
# password = "1234"
# server_name = "localhost\\SQLEXPRESS"
# database_name = "etimetracklite1"

# # SQL Alchemy database URL for connecting to MS SQL Server
# SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"

# # Create SQLAlchemy engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Define a MetaData object
# metadata = MetaData()

# Define the table schema manually
# items_table = Table(
#     'Login', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('email',Text ),
#     Column('password_hash', Text)
# )

# # Sample data to be inserted
# data_to_insert = [
#     {"id": "12234","email": "john3@example.com", "password_hash": "hash3"},
#     {"id": "12456","email": "johndoe4@example.com", "password_hash": "hash4"},
#     # Add more data as needed
# ]

# with engine.connect() as connection:
#     # Build the insert statement
#     stmt = insert(items_table).values(data_to_insert)

#     # Execute the insert statement
#     result = connection.execute(stmt)

#     # Commit the transaction
#     connection.commit()


# with engine.connect() as connection:
#     # Execute a SELECT query to retrieve data from the table
#     query = items_table.select()
#     result = connection.execute(query)

#     # Fetch all rows from the result
#     rows = result.fetchall()

#     # Print the column names
#     print("Column Names:", items_table.columns.keys())

#     # Print the data from the table
#     print("Table Data:")
#     for row in rows:
#         print(row)



# ======================================================= dont touch the above code(its running don't know how) =================================================================


from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

# for hashing
from passlib.context import CryptContext

# for login
from sqlalchemy.sql import select
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

#select
from sqlalchemy.sql import text
from sqlalchemy import select


# Import UnknownHashError from Passlib
from passlib.exc import UnknownHashError

# Define your connection parameters
username = "neel"
password = "1234"
server_name = "localhost\\SQLEXPRESS"
database_name = "etimetracklite1"

# SQL Alchemy database URL for connecting to MS SQL Server
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Define a MetaData object
metadata = MetaData()

# Define the table schema manually
login_table = Table(
    'Login', metadata,
    Column('id', Integer, primary_key=True),
    Column('email',Text ),
    Column('password_hash', Text)
)

# Initialize FastAPI
app = FastAPI()

# Pydantic model for user registration data
class UserRegistration(BaseModel):
    email: str
    password_hash: str


# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to check if user with the given email already exists
def get_user_check(email: str):
    with engine.connect() as connection:
        stmt = login_table.select().where(login_table.c.email == email)
        result = connection.execute(stmt)
        return result.fetchone() is not None

# Register route to insert user data into the database
@app.post("/register/")
def register_user(user_data: UserRegistration):
    # Check if the email already exists
    if get_user_check(user_data.email):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Hash the password
    hashed_password = pwd_context.hash(user_data.password_hash)

    try:
        with engine.connect() as connection:
            # Build the insert statement
            stmt = login_table.insert().values(
                email=user_data.email,
                password_hash=hashed_password
            )

            # Execute the insert statement
            result = connection.execute(stmt)

            # Commit the transaction
            connection.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Error occurred while registering user")

    return {"message": "User registered successfully"}



SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Pydantic model for the access token
class Token(BaseModel):
    access_token: str
    token_type: str




# # Function to verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
    
# Function to verify password
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        raise HTTPException(status_code=500, detail="Unknown hash algorithm used")
    


# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Endpoint for user login and authentication
# @app.post("/login", response_model=Token)
# async def login(user: UserRegistration):
#     # Create session
#     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     session = Session()

#     try:
#         # Query the user from the database
#         # stmt = select([login_table]).where(login_table.c.email == user.email)
#         stmt = text(f"SELECT * FROM Login WHERE email = '{user.email}'")
#         result = session.execute(stmt)
#         db_user = result.fetchone()


#         # Check if user exists and password is correct
#         if db_user and verify_password(user.password_hash, db_user.password_hash):
#             access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#             access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
#             return {"access_token": access_token, "token_type": "bearer"}

#         # If user not found or password is incorrect, raise HTTPException
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
#     finally:
#         session.close()


@app.post("/login", response_model=Token)
async def login(user: UserRegistration):
    # Create session
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    try:
        # Query the user from the database
        stmt = text(f"SELECT * FROM Login WHERE email = '{user.email}'")
        result = session.execute(stmt)
        db_user = result.fetchone()

        print("DB User:", db_user)  # Print fetched user for debugging

        # Check if user exists and password is correct
        if db_user and verify_password(user.password_hash, db_user.password_hash):  # Fix here
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}

        # If user not found or password is incorrect, raise HTTPException
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    finally:
        session.close()
