from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
    # Validate input
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
    # Validate input
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
