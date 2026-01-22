from datetime import datetime
import os
from pydantic import BaseModel, ConfigDict
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    confirm_password: Optional[str] = None
    is_staff: Optional[bool] = True
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "amir",
                "email": "amir@gmail.com",
                "password": "123456",
                "confirm_password": "123456",
                "is_staff": False,
                "is_active": True,
            }
        },
    )

class SignInModel(BaseModel):
    username_or_email: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username_or_email": "amir@gmail.com",
                "password": "123456",
                "username": "amir",
            }
        },
    )

class Token(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-secret")
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False