# HowsTheWeather

기존 날씨 앱의 느린 업데이트와 숫자로 표현된 기온의 한계를 개선하여, 실시간 채팅 기능을 통해 사용자들이 생생한 현재 날씨를 공유하고 빠르게 날씨 변화를 감지할 수 있는 새로운 날씨 웹사이트입니다.

## 프로젝트 설명

기존 날씨 앱/웹들의 즉각적인 현재 날씨 변화의 업데이트가 느린 점, 기온을 나타내는 숫자로는 체감온도를 현실감 있게 표현 불가능하다는 점을 개선하고자 제작되었습니다. 기존 날씨 정보 기능은 그대로 제공하되, 실시간 채팅기능으로 사람들 간의 소통을 할 수 있도록 하여 생생한 현재 날씨를 서로 공유하고 날씨 변화를 더 빠르게 캐치할 수 있도록 합니다.

### 주요 기능
- **실시간 채팅기능**: 사용자 간 실시간으로 날씨 정보를 공유합니다.
- **지역 검색 기능**: 특정 지역의 날씨 정보를 검색할 수 있습니다.
- **현재 위치 기반 날씨 연동 기능**: 사용자의 현재 위치를 기반으로 날씨 정보를 제공합니다.

## 설치

다음 명령어를 사용하여 필요한 패키지들을 설치할 수 있습니다:

```bash
pip install fastapi uvicorn sqlalchemy pandas jinja2 openpyxl databases
```

## 사용법

이 git repository를 clone하여 사용한다면 HowsTheWeather 폴더 안으로 이동한 후 uvicorn 명령어를 실행해주세요.

```bash
cd HowsTheWeather
```
```bash
uvicorn app.main:app
```

이후 명령어 밑에 뜨는 
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
여기에서 주소를 ctrl키를 누른채로 클릭하면 웹사이트 창이 나타납니다.
