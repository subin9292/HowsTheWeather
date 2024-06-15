from fastapi import FastAPI
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 여기에 라우터 및 기타 초기화 코드를 추가할 수 있습니다.
