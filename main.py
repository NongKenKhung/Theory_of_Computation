from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

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
            columns=["number", "name", "image", "type","stats"]
        )
        return StreamingResponse(
            iter([df.to_csv(index=False)]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=pokemon.csv"}
        )
    except Exception as e:
        return RedirectResponse(url="/", status_code=302)

def get_filtered_data(query: str):
    results = []
    try:
        with open('pokemon_1.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            print(query)
            pattern = re.compile(query, re.IGNORECASE)
            for row in reader:
                if pattern.search(row['Name']):
                    results.ap1pend(row)
    except FileNotFoundError:
        return []
    return results


@app.get("/export-csv")
async def download_file():
    file_path = f"pokemon.csv" # Replace with your actual file path
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/octet-stream", filename=file_path)
    else:
        return {"message": "File not found"}

@app.get("/get-query", response_class=JSONResponse)
async def query(query: str = Query(None, description="The name or regex pattern to search for")):
    results = get_filtered_data(query)
    return results


@app.get("/list-items", response_class=HTMLResponse)
async def read_item(request: Request):
    try:
        with open('pokemon_1.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader) 
            return templates.TemplateResponse(
                "list_crawl.html", {"request": request, "data": csv_reader}
            )
    except Exception as e:
        return Response(status_code=500)

app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="static", html=True), name="static")