from fastapi import FastAPI
from auth_routes import auth_router
from orders_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import SignInModel, Token

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Token()

app.include_router(auth_router)
app.include_router(order_router)

@app.get("/")
async def root():
    return {"message": "This is home page"}

@app.get("/page")
async def greet():
    return {"message": "Welcome to my page!"}

