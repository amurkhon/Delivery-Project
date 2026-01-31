from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from models import User, Product, Order, OrderStatus, ProductStatus
from database import get_db
from schemas import OrderModel, OrderCreateModel, OrderUpdateModel
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from auth_routes import get_current_user

order_router = APIRouter(
    prefix='/order'
)

@order_router.get('/all', status_code=status.HTTP_200_OK, response_model=List[OrderModel])
async def get_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = get_current_user(db, Authorize)
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return jsonable_encoder(orders)

@order_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=OrderModel)
async def create_order(order: OrderCreateModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = get_current_user(db, Authorize)

    if not order.product_ids:
        raise HTTPException(status_code=400, detail='At least one product is required')

    total_amount = 0.0
    products_to_add = []

    for product_id in order.product_ids:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f'Product with id {product_id} not found')
        
        # Check if product is available
        if product.status != ProductStatus.available:
            raise HTTPException(status_code=400, detail=f'Product "{product.name}" is not available')
        
        # Check stock availability
        if product.quantity < 1:
            raise HTTPException(status_code=400, detail=f'Product "{product.name}" is out of stock')
        
        products_to_add.append(product)
        total_amount += product.price

    # Create the order
    new_order = Order(
        user_id=user.id,
        quantity=len(order.product_ids),
        total_amount=total_amount,
        status=OrderStatus.pending
    )
    new_order.user = user

    # Add products to order and decrement stock
    for product in products_to_add:
        new_order.products.append(product)
        product.quantity -= 1

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return jsonable_encoder(new_order)

@order_router.put('/update/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderModel)
async def update_order(order_id: int, order: OrderUpdateModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = get_current_user(db, Authorize)

    target_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not target_order:
        raise HTTPException(status_code=404, detail='Order not found')
    
    target_order.status = order.status
    db.commit()
    db.refresh(target_order)

    return jsonable_encoder(target_order)

@order_router.get('/single/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderModel)
async def get_order(order_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = get_current_user(db, Authorize)
    
    target_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not target_order:
        raise HTTPException(status_code=404, detail='Order not found')
    
    return jsonable_encoder(target_order)
