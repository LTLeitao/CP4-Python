from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

class UserCreate(BaseModel):
    address: str = Field(..., min_length=3)
    email: EmailStr
    cpf: str = Field(..., pattern=r"^\d{11}$")
    plan_id: int = Field(..., gt=0)

class UserUpdate(BaseModel):
    address: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    cpf: Optional[str] = Field(None, pattern=r"^\d{11}$")
    plan_id: Optional[int] = Field(None, gt=0)