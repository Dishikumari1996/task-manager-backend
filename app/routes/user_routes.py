from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.response import APIResponse
from app.models.user import User
from app.db.database import get_db

from app.services.auth_service import hash_password
from app.services.auth_service import verify_password, create_access_token
from app.services.auth_dependency import get_current_user
from app.services.role_dependency import require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=APIResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return APIResponse(
        success=True,
        message="User registered successfully",
        data=UserResponse.model_validate(new_user)
    )

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": existing_user.id,
        "role": existing_user.role
    })

    return APIResponse(
        success=True,
        message="Login successful",
        data={
            "access_token": token,
            "token_type": "bearer"
        }
    )

@router.get("/me", response_model=APIResponse)
def get_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    return APIResponse(
        success=True,
        message="User profile fetched",
        data=UserResponse.model_validate(user)
    )