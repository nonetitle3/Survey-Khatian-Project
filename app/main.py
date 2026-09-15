from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import data_provider as provider

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Survey Khatian API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Survey Khatian API"}


@app.get("/api/divisions")
def divisions():
    return provider.list_divisions()


@app.get("/api/districts")
def districts(division_id: str = Query(..., min_length=1)):
    return provider.list_districts(division_id)


@app.get("/api/upazilas")
def upazilas(district_id: str = Query(..., min_length=1)):
    return provider.list_upazilas(district_id)


@app.get("/api/surveys")
def surveys(upazila_id: str = Query(..., min_length=1)):
    return provider.list_surveys(upazila_id)


@app.get("/api/mouzas")
def mouzas(upazila_id: str = Query(..., min_length=1), survey_id: str = Query(..., min_length=1)):
    return provider.list_mouzas(upazila_id, survey_id)


@app.get("/api/khatians")
def khatians(mouza_id: str = Query(..., min_length=1), q: str = Query("", max_length=100)):
    return provider.list_khatians(mouza_id, q)


@app.get("/api/khatians/{khatian_id}")
def khatian(khatian_id: str):
    row = provider.get_khatian(khatian_id)
    if not row:
        raise HTTPException(status_code=404, detail="Khatian not found")
    return row


@app.get("/api/khatians/{khatian_id}/pdf")
def khatian_pdf(khatian_id: str):
    try:
        path = provider.ensure_demo_pdf(khatian_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Khatian not found") from None
    return FileResponse(path, media_type="application/pdf", filename=path.name)


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
