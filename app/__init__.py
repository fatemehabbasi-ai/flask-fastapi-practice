from fastapi import FastAPI
app = FastAPI()
from .config import Base,engine
Base.metadata.create_all(bind=engine)
from . import routes 




