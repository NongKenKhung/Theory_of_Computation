from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse,RedirectResponse
from crawling import crawling
import pandas as pd

app = FastAPI()

api_router = APIRouter()

@api_router.get("/download/pokemon")
async def get_pokemon():
    try:
        pokemon_list = crawling()
        if not pokemon_list:
            return RedirectResponse(url="/", status_code=302)
        df = pd.DataFrame(
            pokemon_list, 
            columns=["number", "name", "image", "type","stats"]
        )
        return StreamingResponse(
            iter([df.to_csv(index=False)]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=pokemon.csv"}
        )
    except Exception as e:
        return RedirectResponse(url="/", status_code=302)


# set /api for api route
app.include_router(api_router, prefix="/api")

app.mount("/", StaticFiles(directory="static", html=True), name="static")