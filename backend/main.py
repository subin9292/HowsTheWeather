from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="backend/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).all()
    return templates.TemplateResponse("index.html", {"request": request, "comments": comments})

@app.post("/comments/", response_class=RedirectResponse)
async def create_comment(request: Request, name: str = Form(...), comment: str = Form(...), db: Session = Depends(database.get_db)):
    db_comment = models.Comment(name=name, comment=comment)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return RedirectResponse(url="/", status_code=303)

@app.get("/location_search.html", response_class=HTMLResponse)
async def location_search(request: Request):
    return templates.TemplateResponse("location_search.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5500, reload=True)
