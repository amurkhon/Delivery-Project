from contextlib import asynccontextmanager
from alembic.config import Config
from alembic import command
from fastapi import FastAPI
from auth_routes import auth_router
from orders_routes import order_router
from fastapi_jwt_auth import AuthJWT
from products_routes import product_router
from schemas import SignInModel, Token

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run migrations on startup
    run_migrations()
    yield

app = FastAPI(lifespan=lifespan)

@AuthJWT.load_config
def get_config():
    return Token()

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)

@app.get("/")
async def root():
    return {"message": "This is home page"}

@app.get("/page")
async def greet():
    return {"message": "Welcome to my page!"}

