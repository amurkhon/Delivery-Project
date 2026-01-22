from ast import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from models import User, Product, Order, OrderStatus
from database import Session, engine
from schemas import OrderModel, OrderStatusModel, OrderUpdateModel
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix='/order'
)

db = Session(bind=engine)

@order_router.get('/all', status_code=status.HTTP_200_OK, response_model=list[OrderModel])
async def get_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Unauthorized')
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=400, detail='Invalid user')
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return jsonable_encoder(orders)

@order_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=OrderModel)
async def create_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    new_order = Order(user_id=user.id, quantity=order.quantity)
    new_order.user = user
    for product_id in order.products:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail='Product not found')
        new_order.products.append(product)
    db.add(new_order)
    db.commit()
    print("New order created: ", new_order)
    return jsonable_encoder(new_order)

@order_router.put('/update/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderModel)
async def update_order(order_id: int, order: OrderUpdateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    target_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not target_order:
        raise HTTPException(status_code=400, detail='Order not found')
    target_order.status = order.status
    db.commit()
    print("Order updated: ", target_order)
    return jsonable_encoder(target_order)

@order_router.get('/single/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderModel)
async def get_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid access token')
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    target_order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not target_order:
        raise HTTPException(status_code=400, detail='Order not found')
    return jsonable_encoder(target_order)