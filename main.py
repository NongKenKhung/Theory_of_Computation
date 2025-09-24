import csv
import json
import re
import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="static/templates")

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

csv_reader