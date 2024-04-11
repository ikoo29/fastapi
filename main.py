from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI()

@app.post("/get-coordinates/")
async def get_coordinates(road: str, num: str):
    full_address = f"{road} {num}"
    url = 'https://api.vworld.kr/req/address'
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": full_address,
        "format": "json",
        "type": "road",
        "key": os.getenv('VWORLD_API_KEY')  # 환경변수에서 API 키 가져오기
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="API call failed")

        data = response.json()
        try:
            # API 응답에서 좌표 추출
            x = data['response']['result']['point']['x']
            y = data['response']['result']['point']['y']
            return {"message": f"{full_address}의 좌표는 x: {x}, y: {y}"}
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid data received from API")
