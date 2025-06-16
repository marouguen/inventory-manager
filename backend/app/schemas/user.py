from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

# Used for incoming registration data
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Used for reading user details (response)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str
    profile_pic: Optional[str] = None

    class ConfigDict:
        from_attributes = True  # Pydantic v2

class UserUpdateRole(BaseModel):
    role: Literal["user", "admin"]