from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

API_KEY = "lwhYf/vFIhpTQsO8X+KBDA==6tqLSK3dHrNxxiL3"  # API-ключ напрямую в коде

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/quote")
async def get_quote():
    url = "https://api.api-ninjas.com/v1/quotes"
    headers = {"X-Api-Key": API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()  # Удалено лишнее await
            if data:
                return {"content": data[0]["quote"], "author": data[0]["author"]}
            return JSONResponse(status_code=404, content={"error": "No quote found"})
    except httpx.HTTPStatusError as e:
        print("API returned non-200:", e.response.status_code, e.response.text)
        return JSONResponse(status_code=500, content={"error": f"API error: {e.response.text}"})
    except Exception as e:
        print("Unexpected error:", str(e))
        return JSONResponse(status_code=500, content={"error": f"Unexpected error: {str(e)}"})
