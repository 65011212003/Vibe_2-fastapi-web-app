from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import PyJWTError
from app.models.auth import UserRegister, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService, SECRET_KEY, ALGORITHM

router = APIRouter(tags=["auth"])
auth_service = AuthService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user."""
    try:
        user = auth_service.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Authenticate a user and return a token."""
    user = auth_service.authenticate_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with user ID as the subject
    token = auth_service.create_access_token(data={"sub": user.id, "username": user.username})
    return token


async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """Validate token and return the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
        
    # Get user from database
    user = auth_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
        
    return user


@router.get("/users/me", response_model=UserResponse)
async def get_current_user(current_user: UserResponse = Depends(get_current_user_from_token)):
    """Get the current authenticated user."""
    return current_user 