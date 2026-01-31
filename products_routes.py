


from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from database import Session, engine

from models import Product, ProductStatus
from schemas import ProductDeleteModel, ProductInquiryModel, ProductModel


product_router = APIRouter(
    prefix='/product'
)

db = Session(bind=engine)

@product_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ProductModel)
async def create_product(product: ProductModel, Authorize: AuthJWT = Depends()):
    print("Code is running before Authorize.jwt_required()...")
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    new_product = Product(
        name=product.name, 
        price=product.price, 
        quantity=product.quantity, 
        product_category=product.product_category,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    print("new_product: ", jsonable_encoder(new_product))
    print("Code is running before new_product.commit()...")
    db.add(new_product)
    print("Code is running before db.commit()...")
    db.commit()
    response = {
        'id': new_product.id,
        'name': new_product.name,
        'price': new_product.price,
        'quantity': new_product.quantity,
        'product_category': new_product.product_category,
        'created_at': new_product.created_at,
        'updated_at': new_product.updated_at,
    }
    return response

@product_router.put('/update/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductModel)
async def update_product(product_id: int, product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    target_product = db.query(Product).filter(Product.id == product_id).first()
    if not target_product:
        raise HTTPException(status_code=400, detail='Product not found')
    target_product.name = product.name
    target_product.price = product.price
    target_product.quantity = product.quantity
    target_product.product_category = product.product_category
    db.commit()
    response = {
        'id': target_product.id,
        'name': target_product.name,
        'price': target_product.price,
        'quantity': target_product.quantity,
        'product_category': target_product.product_category,
        'status': target_product.status,
        'created_at': target_product.created_at,
        'updated_at': target_product.updated_at,
    }
    return response

@product_router.get('/single/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductModel)
async def get_product(product_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    target_product = db.query(Product).filter(Product.id == product_id).first()
    if not target_product:
        raise HTTPException(status_code=400, detail='Product not found')
    response = {
        'id': target_product.id,
        'name': target_product.name,
        'price': target_product.price,
        'quantity': target_product.quantity,
        'product_category': target_product.product_category,
        'status': target_product.status,
        'created_at': target_product.created_at,
        'updated_at': target_product.updated_at,
    }
    return response

@product_router.put('/delete/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductModel)
async def delete_product(product_id: int, payload: ProductDeleteModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    target_product = db.query(Product).filter(Product.id == product_id).first()
    if not target_product:
        raise HTTPException(status_code=400, detail='Product not found')
    target_product.status = payload.status
    db.commit()
    response = {
        'id': target_product.id,
        'name': target_product.name,
        'price': target_product.price,
        'quantity': target_product.quantity,
        'product_category': target_product.product_category,
        'status': target_product.status,
        'created_at': target_product.created_at,
        'updated_at': target_product.updated_at,
    }
    return response

@product_router.get('/all', status_code=status.HTTP_200_OK, response_model=list[ProductModel])
async def get_products(payload: ProductInquiryModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    products = db.query(Product).filter(Product.status == payload.status).all()
    if not products:
        raise HTTPException(status_code=404, detail="No data found")
    response = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': product.quantity,
                'product_category': product.product_category,
                'status': product.status,
                'created_at': product.created_at,
                'updated_at': product.updated_at,
            } for product in products
    ]

    return response