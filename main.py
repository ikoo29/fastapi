from fastapi import FastAPI, Query
import httpx
import os

app = FastAPI()

@app.get("/get-coordinates/")
async def get_coordinates(ads: str = Query(...), num: str = Query(...)):
    full_ads = ads + str(num)
    url = 'https://api.vworld.kr/req/address'
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": full_ads,
        "format": "json",
        "type": "road",
        "key": os.environ('key_num')
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
            
        # API 응답에서 좌표 추출
        x = data['response']['result']['point']['x']
        y = data['response']['result']['point']['y']
        return {"message" : full_ads + "의 좌표의 x값은 " + x + ", y값은 " + y + "입니다."}

