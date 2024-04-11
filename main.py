from fastapi import FastAPI, Query, HTTPException
import httpx

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
        "key": "6F8A7554-1FF8-33C3-83EC-2B74113F97BD" 
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()  # 4xx, 5xx 응답을 예외로 처리
        data = response.json()
            
        # API 응답에서 좌표 추출
        x = data['response']['result']['point']['x']
        y = data['response']['result']['point']['y']
        return {"message" : full_ads + "의 좌표의 x값은 " + x + ", y값은 " + y + "입니다."}

