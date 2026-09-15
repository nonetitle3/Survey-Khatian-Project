from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


def test_hierarchy_and_search():
    assert client.get('/api/divisions').status_code == 200
    assert client.get('/api/districts?division_id=mymensingh').status_code == 200
    assert client.get('/api/upazilas?district_id=mymensingh').status_code == 200
    assert client.get('/api/surveys?upazila_id=trishal').status_code == 200
    assert client.get('/api/mouzas?upazila_id=trishal&survey_id=rs').status_code == 200
    rows = client.get('/api/khatians?mouza_id=trishal-rs-01&q=101')
    assert rows.status_code == 200
    assert rows.json()[0]['khatian_no'] == '101'


def test_pdf_endpoint():
    r = client.get('/api/khatians/k-101/pdf')
    assert r.status_code == 200
    assert r.headers['content-type'] == 'application/pdf'
    assert r.content.startswith(b'%PDF')
