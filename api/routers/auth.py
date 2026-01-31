from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from api.core.database import supabase
from api.models.auth import UserSignup, UserLogin, Token
from api.models.schemas import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/signup", response_model=Token)
async def signup(user: UserSignup):
    try:
        # Since Supabase Auth REQUIRES an email, we will auto-generate a fake email based on username
        # Format: {username}@hots.local
        # This is invisible to the user
        fake_email = f"{user.username}@hots.local"
        
        # Sign up with Supabase Auth using Admin API (bypasses "Signups disabled" and "Confirm email")
        try:
            # Note: supabase-py client initialized with service_role key has admin privileges
            auth_response = supabase.auth.admin.create_user({
                "email": fake_email,
                "password": user.password,
                "email_confirm": True, # Auto confirm email
                "user_metadata": {
                    "username": user.username
                }
            })
        except Exception as auth_error:
            print(f"Supabase Auth Error: {auth_error}")
            error_msg = str(auth_error).lower()
            
            if "rate limit" in error_msg:
                raise HTTPException(
                    status_code=429, 
                    detail="Too many attempts. Please wait a while or try a different username."
                )
                
            if hasattr(auth_error, "message"):
                raise HTTPException(status_code=400, detail=auth_error.message)
            if hasattr(auth_error, "msg"):
                raise HTTPException(status_code=400, detail=auth_error.msg)
            raise HTTPException(status_code=400, detail=str(auth_error))
        
        # Admin create_user returns User object directly, not Session
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Signup failed: No user returned")

        # Create user record in our users table
        # Now handled by Postgres Trigger (on_auth_user_created) automatically
        
        # Since admin.create_user doesn't return a session, we need to sign in to get one
        try:
            login_response = supabase.auth.sign_in_with_password({
                "email": fake_email,
                "password": user.password
            })
            
            return {
                "access_token": login_response.session.access_token if login_response.session else "",
                "token_type": "bearer",
                "user": {
                    "id": auth_response.user.id,
                    "username": user.username
                }
            }
        except Exception as login_error:
             print(f"Auto-login after signup failed: {login_error}")
             msg = str(login_error)
             if "Email logins are disabled" in msg:
                 raise HTTPException(status_code=400, detail="请在 Supabase 后台开启 Email Provider (Authentication -> Providers -> Email -> Enable Email provider)")
             
             # Return the specific error to help debugging
             raise HTTPException(status_code=400, detail=f"User created. Login failed: {msg}")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    try:
        # Construct the fake email from username
        fake_email = f"{user.username}@hots.local"
        
        auth_response = supabase.auth.sign_in_with_password({
            "email": fake_email,
            "password": user.password
        })
        
        # Check if user exists but session is missing (could be unconfirmed email)
        if auth_response.user and not auth_response.session:
             pass

        if not auth_response.user or not auth_response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        # Fetch username from our users table
        db_user = supabase.table("users").select("username").eq("id", auth_response.user.id).single().execute()
        username = db_user.data.get("username") if db_user.data else user.username

        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                # "email": username, # Removed
                "username": username
            }
        }
    except Exception as e:
        # If it's a "Email not confirmed" error, we can't easily bypass it without changing Supabase project settings.
        # But we can try to use the Admin API to auto-confirm user if we had the service role key?
        # We do have the service role key in .env!
        raise HTTPException(status_code=400, detail=str(e))

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
