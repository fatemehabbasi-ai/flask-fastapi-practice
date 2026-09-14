from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from fastapi import Depends
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = FastAPI()

engine = create_engine("sqlite:///fastapi_users.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    
Base.metadata.create_all(bind=engine)


class LoginData(BaseModel):
    username: str
    password: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def say_hello():
    return {"message": "Hello!"}

@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message":f"Hello,{name}!"}

@app.get("/age/{age}")
def age_user(age:int):
    age = 100 - age
    return {"message":f"You will turn 100 in {age} years!"}
    
@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if user and check_password_hash(user.password, data.password):
        return {"status": "success", "message": "Login successful!"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
                
@app.post("/register")
def register(data: LoginData,db:Session=Depends(get_db)):
    hashed_password = generate_password_hash(data.password)
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=data.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"status": "success", "message": "User registered!"}