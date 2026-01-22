import datetime
from sqlalchemy.sql._elements_constructors import or_
from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from schemas import SignInModel, SignUpModel
from database import Session, engine
from models import User
from fastapi import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix='/auth'
)

db = Session(bind=engine)

@auth_router.get('/')
async def signup_auth(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return {'message': 'This is auth route signup page!'}

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    if user.confirm_password is not None and user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail='Passwords do not match')
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail='User already exists')
    new_user = User(
        username=user.username, 
        email=user.email, 
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'is_active': new_user.is_active,
        'is_staff': new_user.is_staff,
        'created_at': new_user.created_at,
        'updated_at': new_user.updated_at,
    }
    return response

@auth_router.post('/signin', status_code=status.HTTP_200_OK)
async def signin(user: SignInModel, Authorize: AuthJWT = Depends()):
    # user_exists = db.query(User).filter(User.email == user.email).first()

    # username or email
    user_exists = db.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email,
        )
    ).first()
    if not user_exists:
        raise HTTPException(status_code=400, detail='Invalid username or email!')

    if user_exists and check_password_hash(user_exists.password, user.password):
        access_token = Authorize.create_access_token(subject=user_exists.username)
        refresh_token = Authorize.create_refresh_token(subject=user_exists.username)
        token = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Successfully logged in",
            "token": token,
        }
        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)
        return jsonable_encoder(response)
    raise HTTPException(status_code=400, detail='Invalid email or password')



    @auth_router.get('/signin/refresh')
    async def refresh_token(Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required() # access token is required
            current_user = Authorize.get_jwt_subject() # get the user from the access token

            # check if the user exists
            user = db.query(User).filter(User.username == current_user).first()
            if not user:
                raise HTTPException(status_code=400, detail='Invalid user')
            access_token = Authorize.create_access_token(subject=user.username)
            refresh_token = Authorize.create_refresh_token(subject=user.username)
            token = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            response = {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Successfully refreshed token",
                "token": token,
            }
            Authorize.set_access_cookies(access_token)
            Authorize.set_refresh_cookies(refresh_token)
            return jsonable_encoder(response)
        except Exception as e:
            raise HTTPException(status_code=401, detail='Unauthorized')
