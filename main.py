from fastapi import FastAPI, HTTPException, Header, Depends, Security
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
from auth import supabase

app = FastAPI(
    title="Auth API",
    description="Secure API with Supabase Auth",
    version="1.0.0"
)
security = HTTPBearer()
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

def get_current_user(credentials = Security(security)):
    """Reusable dependency that verifies the JWT token."""
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        return {"user": user_response.user, "token": token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
# ============================================
# PUBLIC ROUTE (no auth required)
# ============================================
@app.get("/public/info", summary="Public info - no auth needed")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# ============================================
# PROTECTED ROUTE (now with token verification)
# ========================
@app.get("/protected/profile", summary="Get user profile - via dependency")
def get_profile(current=Depends(get_current_user)):
    user = current["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at)
    }
@app.get("/protected/dashboard", summary="Dashboard - protected")
def dashboard(current=Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {current['user'].email}",
        "user_id": current["user"].id
    }


@app.post("/auth/logout", status_code=204, summary="Logout")
def logout(current=Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
