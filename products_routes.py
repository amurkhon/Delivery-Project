from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from database import get_db
from models import Product, ProductStatus, UserRole
from schemas import ProductDeleteModel, ProductModel
from auth_routes import get_current_user, require_admin

product_router = APIRouter(
    prefix='/product'
)

@product_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ProductModel)
async def create_product(product: ProductModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # Only admin can create products
    require_admin(db, Authorize)
    
    new_product = Product(
        name=product.name, 
        price=product.price, 
        quantity=product.quantity, 
        product_category=product.product_category,
        status=product.status or ProductStatus.available,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return jsonable_encoder(new_product)

@product_router.put('/update/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductModel)
async def update_product(product_id: int, product: ProductModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # Only admin can update products
    require_admin(db, Authorize)
    
    target_product = db.query(Product).filter(Product.id == product_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail='Product not found')
    
    target_product.name = product.name
    target_product.price = product.price
    target_product.quantity = product.quantity
    target_product.product_category = product.product_category
    target_product.updated_at = datetime.now()
    
    db.commit()
    db.refresh(target_product)
    
    return jsonable_encoder(target_product)

@product_router.get('/single/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductModel)
async def get_product(product_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    get_current_user(db, Authorize)
    
    target_product = db.query(Product).filter(Product.id == product_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail='Product not found')
    
    return jsonable_encoder(target_product)

@product_router.delete('/delete/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductModel)
async def delete_product(product_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    # Only admin can delete products
    require_admin(db, Authorize)
    
    target_product = db.query(Product).filter(Product.id == product_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail='Product not found')
    
    # Soft delete by setting status to deleted
    target_product.status = ProductStatus.deleted
    target_product.updated_at = datetime.now()
    
    db.commit()
    db.refresh(target_product)
    
    return jsonable_encoder(target_product)

@product_router.get('/all', status_code=status.HTTP_200_OK, response_model=List[ProductModel])
async def get_products(
    status_filter: Optional[ProductStatus] = Query(default=ProductStatus.available, alias="status"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    get_current_user(db, Authorize)
    
    products = db.query(Product).filter(Product.status == status_filter).all()
    if not products:
        return []
    
    return jsonable_encoder(products)
