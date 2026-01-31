from datetime import datetime
import os
from pydantic import BaseModel, ConfigDict
from typing import Optional

from models import ProductCategory, ProductStatus, UserRole

class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    confirm_password: str
    is_staff: Optional[bool] = True
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    role: str

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
                "role": UserRole.admin,
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

class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    user_id: Optional[int]
    product_id: Optional[int]
    total_amount: Optional[float]
    status: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 1,
                "user_id": 1,
                "product_id": 1,
                "total_amount": 100.00,
                "status": "PENDING",
            }
        }

class OrderStatusModel(BaseModel):

    order_statuses: Optional[str] = "PENDING"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "PENDING",
            }
        }

class OrderUpdateModel(BaseModel):
    status: Optional[str]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "status": "PENDING",
            }
        }

class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    price: float
    quantity: int
    created_at: Optional[datetime]
    status: Optional[ProductStatus]
    product_category: ProductCategory

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Product 1",
                "price": 100.00,
                "quantity": 1,
                "status": "available",
                "product_category": ProductCategory.food,
            }
        }

class ProductDeleteModel(BaseModel):
    status: ProductStatus
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "status": "deleted",
            }
        }
class ProductInquiryModel(BaseModel):
    status: ProductStatus
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "status": "available"
            }
        }