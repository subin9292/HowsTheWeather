from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import pandas as pd
from app import models, database
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Static files configuration
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Database tables creation
models.Base.metadata.create_all(bind=database.engine)

# Excel file path
file_path = 'data/location_data.xlsx'

# Read Excel file
df = pd.read_excel(file_path)
df_selected = df[['1단계', '2단계', '격자 X', '격자 Y', '경도(시)', '경도(분)', '경도(초)', '위도(시)', '위도(분)', '위도(초)']]
df_unique = df_selected.drop_duplicates(subset=['1단계', '2단계'])

# Extract unique regions
region_list = df_unique['1단계'].unique().tolist()

# Root endpoint - redirects to default region (서울 in this example)
@app.get("/", response_class=HTMLResponse)
async def redirect_to_default_region():
    return RedirectResponse(url="/comments/서울")

# Endpoint to display comments by region
@app.get("/comments/{region}", response_class=HTMLResponse)
async def read_comments_by_region(request: Request, region: str, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.region == region).all()
    logging.info(f"Fetched comments for region: {region}, Count: {len(comments)}") # 로그 추가
    return templates.TemplateResponse("main.html", {
        "request": request,
        "comments": comments,
        "region": region,
        "regions": region_list
    })

# Endpoint to create comments for a specific region
@app.post("/comments/{region}/add", response_class=HTMLResponse)
async def create_comment_by_region(region: str, name: str = Form(...), comment: str = Form(...), db: Session = Depends(database.get_db)):
    logging.info(f"Received new comment for region: {region} - Name: {name}, Comment: {comment}") # 로그 추가
    db_comment = models.Comment(name=name, comment=comment, region=region)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return RedirectResponse(url=f"/comments/{region}", status_code=303)

# Endpoint serving location_search.html
@app.get("/location_search", response_class=HTMLResponse)
async def location_search(request: Request):
    return templates.TemplateResponse("location_search.html", {"request": request})

# Endpoint to serve main.html directly (not typically needed but included for completeness)
@app.get("/main.html", response_class=HTMLResponse)
async def read_main():
    with open("templates/main.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# Endpoint to serve location_search.html directly (not typically needed but included for completeness)
@app.get("/location_search.html", response_class=HTMLResponse)
async def read_location_search():
    with open("templates/location_search.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# Search endpoint for locations
@app.get("/search")
def search(query: str):
    query = query.lower()
    results = df_unique[(df_unique['1단계'].str.contains(query, case=False, na=False)) | 
                        (df_unique['2단계'].str.contains(query, case=False, na=False))]
    
    places = results[['1단계', '2단계']].drop_duplicates().apply(lambda row: " ".join(row.dropna()), axis=1).tolist()
    logging.info(f"Search query: {query}, Results: {places}") # 로그 추가
    return {"places": places}

# Coordinates endpoint for locations
@app.get("/coordinates")
def coordinates(place: str):
    place_parts = place.split()
    
    if len(place_parts) == 1:
        results = df_unique[df_unique['1단계'].str.contains(place_parts[0], case=False, na=False)]
    elif len(place_parts) == 2:
        results = df_unique[(df_unique['1단계'].str.contains(place_parts[0], case=False, na=False)) & 
                            (df_unique['2단계'].str.contains(place_parts[1], case=False, na=False))]
    else:
        raise HTTPException(status_code=400, detail="Invalid place format")
    
    if not results.empty:
        result = results.iloc[0]
        nx, ny = result['격자 X'], result['격자 Y']
        lat = result['위도(시)'] + result['위도(분)'] / 60 + result['위도(초)'] / 3600
        lon = result['경도(시)'] + result['경도(분)'] / 60 + result['경도(초)'] / 3600
        logging.info(f"Coordinates for {place} - X: {nx}, Y: {ny}, Lat: {lat}, Lon: {lon}") # 로그 추가
        return {"message": f"Coordinates for {place} are X: {nx}, Y: {ny}", "coordinates": {"lat": lat, "lon": lon}}
    else:
        logging.error(f"Location not found for {place}") # 에러 로그 추가
        raise HTTPException(status_code=404, detail="Location not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
