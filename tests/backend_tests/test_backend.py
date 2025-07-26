from pathlib import Path

from starlette.testclient import TestClient

from backend.main import app

client = TestClient(app)

current_dir = Path(__file__).parent

lovely_path = current_dir.joinpath("../resources/lovely.pdf")

def test_pdf_to_apl():
    with open(lovely_path, "rb") as f:
        response = client.post("/pdf_to_apl/", files={"file": ("lovely.pdf", f, "application/pdf")})

    assert response.status_code == 200

def test_pdf_query_with_valid_cookie():
    with open(lovely_path, "rb") as f:
        response = client.post("/pdf_to_apl/", files={"file": ("lovely.pdf", f, "application/pdf")})

    cookie = response.cookies

    