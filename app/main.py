#지역검색에서 지역을 선택하여도 선택한 지역의 정보 화면으로 넘어가지지 않는 상황은 개선해야할 부분임
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import pandas as pd
from . import models
from .database import get_db, engine

app = FastAPI()

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 엑셀 파일 경로
file_path = 'data/location_data.xlsx'

# 엑셀 파일 읽기
df = pd.read_excel(file_path)
df_selected = df[['1단계', '2단계', '격자 X', '격자 Y', '경도(시)', '경도(분)', '경도(초)', '위도(시)', '위도(분)', '위도(초)']]
df_unique = df_selected.drop_duplicates(subset=['1단계', '2단계'])

# 루트 엔드포인트: 메인 페이지 렌더링
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, lat: float = None, lon: float = None, db: Session = Depends(get_db)):
    location_key = f"{lat:.6f},{lon:.6f}" if lat and lon else None
    comments = []
    if location_key:
        comments = db.query(models.Comment).filter(models.Comment.location_key == location_key).all()
        print(f"Fetching comments for location_key: {location_key}, found: {len(comments)} comments")
    else:
        comments = db.query(models.Comment).all()  # 전체 댓글 가져오기

    # 디버깅을 위한 출력
    print(f"Request received with lat: {lat}, lon: {lon}")

    # 템플릿에 데이터를 전달
    return templates.TemplateResponse("main.html", {
        "request": request,
        "comments": comments,
        "lat": lat,
        "lon": lon,
        "location_key": location_key
    })

# 리다이렉션 엔드포인트: /main.html로 접근하면 루트 경로로 리다이렉트
@app.get("/main.html", response_class=RedirectResponse)
async def redirect_to_root():
    return RedirectResponse(url="/")

# 댓글 생성 엔드포인트
@app.post("/comments/", response_class=RedirectResponse)
async def create_comment(
    name: str = Form(...),
    comment: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    db: Session = Depends(get_db)
):
    if not name or not comment:
        raise HTTPException(status_code=422, detail="Name and comment cannot be empty")
    if lat is None or lon is None:
        raise HTTPException(status_code=422, detail="Latitude and Longitude must be provided")
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise HTTPException(status_code=422, detail="Invalid latitude or longitude")

    print(f"Received form data - name: {name}, comment: {comment}, lat: {lat}, lon: {lon}")

    location_key = f"{lat:.6f},{lon:.6f}"
    db_comment = models.Comment(name=name, comment=comment, location_key=location_key)
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        print(f"Comment saved successfully: {db_comment}")
    except Exception as e:
        db.rollback()
        print(f"Error saving comment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return RedirectResponse(url=f"/?lat={lat:.6f}&lon={lon:.6f}", status_code=303)

# 지역 검색 엔드포인트
@app.get("/location_search", response_class=HTMLResponse)
async def location_search(request: Request):
    return templates.TemplateResponse("location_search.html", {"request": request})

# location_search.html 파일 제공 엔드포인트
@app.get("/location_search.html", response_class=HTMLResponse)
async def read_location_search():
    with open("templates/location_search.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# 검색 엔드포인트
@app.get("/search")
def search(query: str):
    query = query.lower()
    results = df_unique[(df_unique['1단계'].str.contains(query, case=False, na=False)) | 
                        (df_unique['2단계'].str.contains(query, case=False, na=False))]
    
    places = results[['1단계', '2단계']].drop_duplicates().apply(lambda row: " ".join(row.dropna()), axis=1).tolist()
    return {"places": places}

# 좌표 엔드포인트
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
        print(f"Coordinates for {place}: (X: {nx}, Y: {ny})")
        return {"message": f"Coordinates for {place} are X: {nx}, Y: {ny}", "coordinates": {"lat": lat, "lon": lon}}
    else:
        raise HTTPException(status_code=404, detail="Location not found")

# 디버그 엔드포인트
@app.get("/check_comments", response_class=HTMLResponse)
def check_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    return {"comments": [c.__dict__ for c in comments]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5500, reload=True)
