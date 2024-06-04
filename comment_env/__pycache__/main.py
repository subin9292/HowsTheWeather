from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# 모듈이 있는 경로가 정확하다면 주석 해제
from comment_env import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="comment_env/templates")

@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(database.get_db)):
    db_comment = models.Comment(name=comment.name, comment=comment.comment)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).all()
    return templates.TemplateResponse("index.html", {"request": request, "comments": comments})

@app.post("/cheongju/comments/", response_model=schemas.Comment)
def create_cheongju_comment(comment: schemas.CommentCreate, db: Session = Depends(database.get_db)):
    db_comment = models.Comment(name=comment.name, comment=comment.comment, location="청주")  # 위치 정보 추가
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/cheongju/", response_class=HTMLResponse)
async def read_cheongju_comments(request: Request, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.location == "청주").all()  # 위치 정보로 필터링
    return templates.TemplateResponse("cheongju_comments.html", {"request": request, "comments": comments})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
