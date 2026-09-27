# Auth API

A secure FastAPI application with Supabase Auth — featuring signup, login, JWT verification, protected routes, and logout.

This project demonstrates how to protect API endpoints using a modern Identity Provider (IdP) instead of rolling your own password system.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI |
| Identity Provider | Supabase |
| Language | Python 3.11 |
| Config | python-dotenv |

---

## Architecture

The app follows a **trust triangle** model:

```
        Client (You)
       /            \
      /              \
     ▼                ▼
 Supabase        FastAPI Server
 (issues JWT)    (verifies JWT)
```

| Step | What Happens |
|------|--------------|
| 1 | Client sends email + password to Supabase via `/auth/signup` or `/auth/login` |
| 2 | Supabase validates and returns a **JWT (access token)** |
| 3 | Client sends requests with `Authorization: Bearer <token>` |
| 4 | FastAPI verifies the token with Supabase before granting access |

---

## Project Structure

```
todo-auth-api/
├── main.py            # FastAPI routes
├── auth.py            # Supabase client setup
├── requirements.txt   # Python dependencies
├── .env.example       # Template for env vars (committed)
├── .env               # Real secrets (GITIGNORED)
├── .gitignore         # Keeps .env out of Git
└── README.md          # This file
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kalaivaniparthi/todo-auth-api.git
cd todo-auth-api
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create your `.env` file

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_public_key
PORT=8000
```

> **Where to find these values:** Supabase Dashboard → Settings → API → Project URL + `anon` public key.

### 4. Run the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## API Reference

| Method | Endpoint | Auth Required | Description |
|--------|----------|:-------------:|-------------|
| POST | `/auth/signup` | ❌ | Create a new user account |
| POST | `/auth/login` | ❌ | Authenticate and receive a JWT |
| POST | `/auth/logout` | ✅ | Terminate the user session |
| GET | `/public/info` | ❌ | Public information (anyone can read) |
| GET | `/protected/profile` | ✅ | Get the authenticated user's profile |
| GET | `/protected/dashboard` | ✅ | Access the protected dashboard |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (login, read) |
| 201 | User created (signup) |
| 204 | Logout successful |
| 400 | Missing or invalid input |
| 401 | Missing, invalid, or expired token |

---

## Testing Flow

1. **Sign up** — `POST /auth/signup` with:
   ```json
   { "email": "test@example.com", "password": "password123" }
   ```

2. **Log in** — `POST /auth/login` with the same credentials.

3. **Copy the `access_token`** from the login response.

4. **Authorize in Swagger** — click the 🔒 **Authorize** button in Swagger UI and paste the token.

5. **Test protected routes** — try `/protected/profile` with **Try it out**. It should return your user info.

6. **Test unauthorized access** — remove the token and try `/protected/profile` again. It should return **401**.

---

## Example Requests

### Signup

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Access protected route

```bash
curl http://localhost:8000/protected/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Public route (no token needed)

```bash
curl http://localhost:8000/public/info
```

---

## Security Notes

- **`.env` is gitignored** — Supabase keys never reach GitHub.
- **Passwords are hashed by Supabase** — my app never sees or stores raw passwords.
- **JWTs are cryptographically verified** on every request via `supabase.auth.get_user(token)`.
- **Reusable dependency** — the `get_current_user` FastAPI dependency protects any route with one line.
- **Bearer token format enforced** — malformed headers are rejected before verification.

---

## What I Learned

- **Identity Providers (IdPs)** like Supabase handle the hard parts of auth safely.
- **JWTs** are self-contained, signed tokens that can't be tampered with.
- **FastAPI dependencies** make auth logic reusable across routes.
- **Swagger UI** can be configured with `HTTPBearer` to show lock icons and an Authorize button.
- **Environment variables** keep secrets out of source code.

---

## Screenshots

### Swagger UI with Authorize button
*(Add screenshot of http://localhost:8000/docs)*

### Login response with access token
*(Add screenshot of successful login)*

### Protected route returning 200
*(Add screenshot of /protected/profile with a valid token)*

### Protected route returning 401
*(Add screenshot of /protected/profile without a token)*

---

## License

Created as part of the **FlyRank AI Backend Engineering Internship** — Week 4, Assignment BE-03.

---

## Author

**Kalaivani Parthi**

- GitHub: [@Kalaivaniparthi](https://github.com/Kalaivaniparthi)
- Project: [todo-auth-api](https://github.com/Kalaivaniparthi/todo-auth-api)
