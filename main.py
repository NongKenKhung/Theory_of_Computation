from fastapi import FastAPI, APIRouter, Query, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse,RedirectResponse, JSONResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import pandas as pd
from crawling import crawling

app = FastAPI()
templates = Jinja2Templates(directory="static/templates")

api_router = APIRouter()

@api_router.get("/download/pokemon")
async def get_pokemon(query: str = Query(None)):
    try:
        pokemon_list = crawling(query)
        if not pokemon_list:
            return RedirectResponse(url="/", status_code=302)
        df = pd.DataFrame(
            pokemon_list, 
            columns=['Number', 'Name', 'Description', 'image', 'Type', 'Species', 'Height', 'Weight', 'All', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        )
        return StreamingResponse(
            iter([df.to_csv(index=False)]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=pokemon.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {e}')

@api_router.get("/list-items", response_class=HTMLResponse)
async def read_item(request: Request, query: str = Query(None)):
    try:
        pokemon_list = crawling(query)
        # all key from pokemon_list
        # ['Number', 'Name', 'Description', 'image', 'Type', 'Species', 
        # 'Height', 'Weight', 'All', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        return templates.TemplateResponse(
            "pokemon_list.html", {"request": request, "data": pokemon_list, "query_text": query}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'{e}')
    except Exception as e:
        print(e)
        return Response(status_code=500)

@app.get("/loading-pokemon", response_class=HTMLResponse)
async def load_pokemon(request: Request, query: str = Query(None)):
    return templates.TemplateResponse('loading_pokemon.html', {"request":request, "query":query})

@app.get("/pokemon-list", response_class=HTMLResponse)
async def pokemon_list(request: Request, query: str = Query(None)):
    return templates.TemplateResponse('pokemon_page.html', {"request":request, "query": query})

@app.get("/user-list", response_class=HTMLResponse)
async def user_list(request:Request):
    return templates.TemplateResponse('user_list.html',{"request":request})

app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="static", html=True), name="static")