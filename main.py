from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from auth import supabase

app = FastAPI(
    title="Auth API",
    description="Secure API with Supabase Auth",
    version="1.0.0"
)

# ============================================
# DATA MODELS
# ============================================
class AuthRequest(BaseModel):
    email: str
    password: str

# ============================================
# SIGN UP
# ============================================
@app.post("/auth/signup", status_code=201, summary="Create a new user account")
def signup(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })
        return {
            "message": "User created successfully",
            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================
# LOGIN
# ============================================
@app.post("/auth/login", summary="Login and receive JWT")
def login(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

# ============================================
# PUBLIC ROUTE (no auth required)
# ============================================
@app.get("/public/info", summary="Public info - no auth needed")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# ============================================
# PROTECTED ROUTE (basic - not verifying yet)
# ============================================
@app.get("/protected/profile", summary="Get user profile - auth required")
def get_profile(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Access token required")
    return {
        "message": "Token received",
        "header": authorization
    }
