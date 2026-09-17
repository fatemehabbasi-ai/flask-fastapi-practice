from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from .config import get_db
from .models import User
from .schemas import LoginData
from . import app

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
