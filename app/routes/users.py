from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import users_collection
from app.utils import hash_password, verify_password, create_jwt_token
from app.schemas import UserSchema, TokenSchema
from app.auth import get_current_user
from app.config import JWT_ALGORITHM
router = APIRouter(prefix="/users", tags=["/users"])

@router.post("/register", response_model=dict)
async def register(user: UserSchema):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    new_user = {"email": user.email, "hashed_password": hashed_password}
    await users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_jwt_token({"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user():
    return {"message":F"""get you all users {JWT_ALGORITHM}"""}
