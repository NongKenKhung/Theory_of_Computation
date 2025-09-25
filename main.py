from fastapi import FastAPI, APIRouter, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse,RedirectResponse, JSONResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import pandas as pd
from crawling import crawling

app = FastAPI()
templates = Jinja2Templates(directory="static/templates")

api_router = APIRouter()

@api_router.get("/download/pokemon")
async def get_pokemon():
    try:
        pokemon_list = crawling()
        if not pokemon_list:
            return RedirectResponse(url="/", status_code=302)
        df = pd.DataFrame(
            pokemon_list, 
            columns=["Number", "Name", "Type", "All", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "image"]
        )
        return StreamingResponse(
            iter([df.to_csv(index=False)]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=pokemon.csv"}
        )
    except Exception as e:
        return RedirectResponse(url="/", status_code=302)

@app.get("/list-items", response_class=HTMLResponse)
async def read_item(request: Request, query: str = Query(None)):
    try:
        pokemon_list = crawling(query)
        return templates.TemplateResponse(
            "list_crawl.html", {"request": request, "data": pokemon_list, "query_text": query}
        )
    except Exception as e:
        return Response(status_code=500)

app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="static", html=True), name="static")