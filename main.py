from fastapi import FastAPI, HTTPException, Request
import httpx
import os

app = FastAPI()

@app.post("/webhook/")
async def get_coordinates(request: Request):
    # 요청 JSON 데이터를 파이썬 객체로 변환
    data = await request.json()
    
    # 'road'와 'num' 추출
    road = data['action']['params']['road']
    num = data['action']['params']['num']
    full_address = f"{road} {num}"
    
    # 외부 API URL 및 파라미터 설정
    url = 'https://api.vworld.kr/req/address'
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": full_address,
        "format": "json",
        "type": "road",
        "key": os.environ['key_num']  # 환경변수에서 API 키 가져오기
    }

    # 외부 API에 비동기 HTTP 요청
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="API call failed")
        
        # API 응답 파싱
        response_data = response.json()
        try:
            x = response_data['response']['result']['point']['x']
            y = response_data['response']['result']['point']['y']
            return {"message": f"{full_address}의 좌표는 x: {x}, y: {y}"}
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid data received from API")

