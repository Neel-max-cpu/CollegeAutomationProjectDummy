from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import randint
from typing import Optional

app = FastAPI()

# Temporary storage for OTPs (in production, you would use a database)
otp_storage = {}


class OTPRequest(BaseModel):
    email: str


class OTPVerification(BaseModel):
    email: str
    otp: int


class User(BaseModel):
    email: str
    password: str


def generate_otp() -> int:
    return randint(1000, 9999)


def send_otp(email: str, otp: int):
    # In a real application, you would send the OTP via email or SMS
    print(f"OTP for {email}: {otp}")


@app.post("/generate_otp/")
async def generate_otp_endpoint(request: OTPRequest):
    otp = generate_otp()
    otp_storage[request.email] = otp  # Store the OTP temporarily
    send_otp(request.email, otp)
    return {"message": "OTP sent successfully"}


@app.post("/verify_otp/")
async def verify_otp_endpoint(verification: OTPVerification):
    stored_otp = otp_storage.get(verification.email)
    if not stored_otp:
        raise HTTPException(status_code=404, detail="OTP not found or expired")
    if stored_otp == verification.otp:
        # Clear the OTP after successful verification
        del otp_storage[verification.email]
        return {"message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")


@app.post("/register/")
async def register_user(user: User):
    # Your registration logic here, after OTP verification
    return {"message": "User registered successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
