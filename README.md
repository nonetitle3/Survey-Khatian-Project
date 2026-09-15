# Survey Khatian Automation

A standalone FastAPI + vanilla JavaScript workflow for authorized Survey Khatian data.

## Workflow

Division → District → Upazila → Survey → Mouza/JL → Khatian → Search → Preview → Download PDF

> This project does **not** scrape, bypass CAPTCHA, bypass authentication, evade rate limits, or reverse-engineer eporcha.tech. Replace the demo provider with data you are authorized to use.

## Windows setup

Requires Python 3.12+ 64-bit.

```bat
setup_windows.bat
run_windows.bat
```

If installation reports that a package has no binary wheel, use a supported 64-bit Python version and rerun setup. The setup script uses binary wheels only, so it will not silently attempt a Rust/Cargo build for pydantic-core.

## Local run

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

## API

- GET /api/health
- GET /api/divisions
- GET /api/districts?division_id=dhaka
- GET /api/upazilas?district_id=mymensingh
- GET /api/surveys?upazila_id=trishal
- GET /api/mouzas?upazila_id=trishal&survey_id=rs
- GET /api/khatians?mouza_id=mouza-1&q=101
- GET /api/khatians/{id}
- GET /api/khatians/{id}/pdf

## Deploy to Render

Use the included `render.yaml`. The service starts with:

`uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Data provider

`app/data_provider.py` contains demo data and the provider interface. Connect your authorized database/API/file source there without changing the frontend workflow.
