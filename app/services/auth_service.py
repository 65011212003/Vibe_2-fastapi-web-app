from typing import Optional, Dict
import uuid
from datetime import datetime, timedelta
import hashlib
import jwt
from app.models.auth import UserRegister, UserLogin, UserResponse, Token
from app.services.db_service import DatabaseService

# This would be in a config file in a real application
SECRET_KEY = "your-secret-key-for-jwt-token"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    """Service for handling user authentication."""
    
    def __init__(self):
        # Initialize database service
        self.db_service = DatabaseService()
    
    def _hash_password(self, password: str) -> str:
        """Hash a password for storing."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a stored password against a provided password."""
        return self._hash_password(plain_password) == hashed_password
    
    def register_user(self, user_data: UserRegister) -> UserResponse:
        """Register a new user."""
        # Check if username already exists
        existing_user = self.db_service.find_one('users', {'username': user_data.username})
        if existing_user:
            raise ValueError("Username already registered")
            
        # Check if email already exists
        existing_email = self.db_service.find_one('users', {'email': user_data.email})
        if existing_email:
            raise ValueError("Email already registered")
        
        # Create user with hashed password
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "password": self._hash_password(user_data.password),
            "full_name": user_data.full_name,
            "created_at": datetime.now().isoformat(),
        }
        
        # Insert user into database
        self.db_service.insert('users', user)
        
        # Return user without password
        user_response = {k: v for k, v in user.items() if k != "password"}
        
        # Convert created_at back to datetime for the response
        if isinstance(user_response["created_at"], str):
            user_response["created_at"] = datetime.fromisoformat(user_response["created_at"])
            
        return UserResponse(**user_response)
    
    def authenticate_user(self, user_data: UserLogin) -> Optional[UserResponse]:
        """Authenticate a user and return user info if valid."""
        user = self.db_service.find_one('users', {'username': user_data.username})
        
        if user and self._verify_password(user_data.password, user["password"]):
            # Return user without password
            user_response = {k: v for k, v in user.items() if k != "password"}
            
            # Convert created_at back to datetime for the response
            if isinstance(user_response["created_at"], str):
                user_response["created_at"] = datetime.fromisoformat(user_response["created_at"])
                
            return UserResponse(**user_response)
            
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get a user by ID."""
        user = self.db_service.find_one('users', {'id': user_id})
        
        if user:
            # Return user without password
            user_response = {k: v for k, v in user.items() if k != "password"}
            
            # Convert created_at back to datetime for the response
            if isinstance(user_response["created_at"], str):
                user_response["created_at"] = datetime.fromisoformat(user_response["created_at"])
                
            return UserResponse(**user_response)
            
        return None
    
    def create_access_token(self, data: dict) -> Token:
        """Create a JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt) 