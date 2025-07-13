from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import uuid
from models import OPSUser, ClientUser, VerifyTable
from models import User, Base
from database import SessionLocal, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Pydantic Schemas
class UserCreate(BaseModel):
    email: str
    password: str
    is_client: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Utility functions
def email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# API Routes
@app.post("/client-register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if email(db, user.email):
        raise HTTPException(status_code=400, detail="email already exists")
    hashed_password = get_password_hash(user.password)
    if user.is_client:
        db_user = ClientUser(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        verify_user = VerifyTable(user_id=db_user.id)
        db.add(verify_user)
        db.commit()
        db.refresh(verify_user)

        # sendMail(email, token)

        return {"msg": "User registered but not yet verified", "email_sent": True}

    db_user = OPSUser(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User registered successfully"}


@app.post("/client-login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token}

@app.get("/verify/")
def verify(verifyLinkID: int, db: Session = Depends(get_db)):
    if db.Query()




