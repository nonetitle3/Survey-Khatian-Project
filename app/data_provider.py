from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)


@dataclass(frozen=True)
class Item:
    id: str
    name: str
    parent_id: str | None = None


DIVISIONS = [Item("dhaka", "ঢাকা"), Item("mymensingh", "ময়মনসিংহ"), Item("sylhet", "সিলেট")]
DISTRICTS = {
    "dhaka": [Item("dhaka", "ঢাকা", "dhaka"), Item("gazipur", "গাজীপুর", "dhaka")],
    "mymensingh": [Item("mymensingh", "ময়মনসিংহ", "mymensingh"), Item("netrokona", "নেত্রকোনা", "mymensingh")],
    "sylhet": [Item("sylhet", "সিলেট", "sylhet"), Item("moulvibazar", "মৌলভীবাজার", "sylhet")],
}
UPAZILAS = {
    "mymensingh": [Item("trishal", "ত্রিশাল", "mymensingh"), Item("muktagacha", "মুক্তাগাছা", "mymensingh")],
    "dhaka": [Item("savar", "সাভার", "dhaka")],
    "sylhet": [Item("sylhet-sadar", "সিলেট সদর", "sylhet")],
}
SURVEYS = {
    "trishal": [Item("rs", "RS", "trishal"), Item("sa", "SA", "trishal")],
    "muktagacha": [Item("rs", "RS", "muktagacha")],
    "savar": [Item("cs", "CS", "savar"), Item("rs", "RS", "savar")],
    "sylhet-sadar": [Item("cs", "CS", "sylhet-sadar")],
}
MOUZAS = {
    "trishal:rs": [Item("trishal-rs-01", "বালিপাড়া (JL 12)", "trishal"), Item("trishal-rs-02", "কানিহার (JL 13)", "trishal")],
    "trishal:sa": [Item("trishal-sa-01", "বালিপাড়া (JL 21)", "trishal")],
    "muktagacha:rs": [Item("muktagacha-rs-01", "দাওগাঁও (JL 07)", "muktagacha")],
    "savar:cs": [Item("savar-cs-01", "আশুলিয়া (JL 03)", "savar")],
    "savar:rs": [Item("savar-rs-01", "বিরুলিয়া (JL 11)", "savar")],
    "sylhet-sadar:cs": [Item("sylhet-cs-01", "খাদিমনগর (JL 05)", "sylhet-sadar")],
}
KHATIANS = {
    "trishal-rs-01": [
        {"id": "k-101", "khatian_no": "101", "owner": "মোঃ আব্দুল করিম", "guardian": "পিং রহমত আলী", "dag_no": "201", "land_area": "0.42 একর"},
        {"id": "k-102", "khatian_no": "102", "owner": "মোছাঃ রহিমা বেগম", "guardian": "স্বামী মোঃ সালাম", "dag_no": "205", "land_area": "0.31 একর"},
    ],
    "trishal-rs-02": [{"id": "k-103", "khatian_no": "103", "owner": "মোঃ সেলিম মিয়া", "guardian": "পিং আব্দুস সাত্তার", "dag_no": "88", "land_area": "0.18 একর"}],
    "trishal-sa-01": [{"id": "k-104", "khatian_no": "55", "owner": "মোঃ হাবিবুর রহমান", "guardian": "পিং কাদের আলী", "dag_no": "71", "land_area": "0.27 একর"}],
    "muktagacha-rs-01": [{"id": "k-105", "khatian_no": "12", "owner": "মোছাঃ নাসিমা আক্তার", "guardian": "পিং আব্দুল হক", "dag_no": "34", "land_area": "0.22 একর"}],
    "savar-cs-01": [{"id": "k-106", "khatian_no": "301", "owner": "মোঃ কামাল হোসেন", "guardian": "পিং মতিউর রহমান", "dag_no": "501", "land_area": "0.15 একর"}],
    "savar-rs-01": [{"id": "k-107", "khatian_no": "410", "owner": "মোঃ জসিম উদ্দিন", "guardian": "পিং কাসেম আলী", "dag_no": "812", "land_area": "0.33 একর"}],
    "sylhet-cs-01": [{"id": "k-108", "khatian_no": "9", "owner": "মোঃ রফিক আহমেদ", "guardian": "পিং আব্দুর রহমান", "dag_no": "19", "land_area": "0.25 একর"}],
}


def _dict(items: list[Item]) -> list[dict[str, Any]]:
    return [asdict(item) for item in items]


def list_divisions() -> list[dict[str, Any]]:
    return _dict(DIVISIONS)


def list_districts(division_id: str) -> list[dict[str, Any]]:
    return _dict(DISTRICTS.get(division_id, []))


def list_upazilas(district_id: str) -> list[dict[str, Any]]:
    return _dict(UPAZILAS.get(district_id, []))


def list_surveys(upazila_id: str) -> list[dict[str, Any]]:
    return _dict(SURVEYS.get(upazila_id, []))


def list_mouzas(upazila_id: str, survey_id: str) -> list[dict[str, Any]]:
    return _dict(MOUZAS.get(f"{upazila_id}:{survey_id}", []))


def list_khatians(mouza_id: str, q: str = "") -> list[dict[str, Any]]:
    rows = KHATIANS.get(mouza_id, [])
    q = q.strip().lower()
    if not q:
        return rows
    return [r for r in rows if any(q in str(r.get(k, "")).lower() for k in ("khatian_no", "owner", "guardian", "dag_no"))]


def get_khatian(khatian_id: str) -> dict[str, Any] | None:
    for mouza_id, rows in KHATIANS.items():
        for row in rows:
            if row["id"] != khatian_id:
                continue
            upazila_id = survey_id = ""
            for key, values in MOUZAS.items():
                if any(item.id == mouza_id for item in values):
                    upazila_id, survey_id = key.split(":", 1)
                    break
            mouza = next((item for item in MOUZAS.get(f"{upazila_id}:{survey_id}", []) if item.id == mouza_id), None)
            district_id = next((district for district, values in UPAZILAS.items() if any(item.id == upazila_id for item in values)), "")
            division_id = next((division for division, values in DISTRICTS.items() if any(item.id == district_id for item in values)), "")
            survey_name = next((item.name for item in SURVEYS.get(upazila_id, []) if item.id == survey_id), survey_id)
            jl = ""
            if mouza and "JL " in mouza.name:
                jl = mouza.name.split("JL ", 1)[1].rstrip(")")
            result = dict(row)
            result.update({
                "division": next((item.name for item in DIVISIONS if item.id == division_id), division_id),
                "district": next((item.name for item in DISTRICTS.get(division_id, []) if item.id == district_id), district_id),
                "upazila": next((item.name for item in UPAZILAS.get(district_id, []) if item.id == upazila_id), upazila_id),
                "survey": survey_name,
                "mouza": mouza.name.split(" (JL", 1)[0] if mouza else mouza_id,
                "jl_no": jl,
                "total_land": row["land_area"],
            })
            return result
    return None


def ensure_demo_pdf(khatian_id: str) -> Path:
    path = STORAGE_DIR / f"{khatian_id}.pdf"
    if path.exists():
        return path
    row = get_khatian(khatian_id)
    if not row:
        raise KeyError(khatian_id)
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    c.setTitle(f"Khatian {row['khatian_no']}")
    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, height - 70, "SURVEY KHATIAN - DEMO COPY")
    c.setFont("Helvetica", 12)
    y = height - 120
    for label, value in [("Khatian No", row["khatian_no"]), ("Owner", row["owner"]), ("Guardian", row["guardian"]), ("Dag No", row["dag_no"]), ("Land Area", row["land_area"]), ("Record ID", row["id"])]:
        c.drawString(60, y, f"{label}: {value}")
        y -= 28
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(60, 70, "Demo PDF generated from authorized/local project data.")
    c.save()
    return path
