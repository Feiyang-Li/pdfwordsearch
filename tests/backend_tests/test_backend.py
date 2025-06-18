from starlette.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_pdf_to_apl():
    with open("../resources/lovely.pdf", "rb") as f:
        response = client.post("/pdf_to_apl/", files={"file": ("lovely.pdf", f, "application/pdf")})

    assert response.status_code == 200


def test_pdf_query_with_invalid_cookie():
    response = client.post("/apl/command/hello")

    assert response.status_code == 403

def test_pdf_query_with_valid_cookie():
    with open("../resources/lovely.pdf", "rb") as f:
        response = client.post("/pdf_to_apl/", files={"file": ("lovely.pdf", f, "application/pdf")})

    cookie = response.cookies

    