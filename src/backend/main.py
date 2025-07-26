import uuid

import pymupdf
from fastapi import FastAPI, File, UploadFile, Form, Cookie, HTTPException
from fastapi.responses import JSONResponse
import os

from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from typing import List, Optional, Annotated, Dict, cast
from pydantic import BaseModel

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
htmlPayload = {}
# Storage (RAM for now but can be changed to disk storage later)
apl_store : Dict[Cookie, CompressedPostingsList] = dict()

class HtmlPayload(BaseModel):
    url: str
    html: str

@app.post("/upload/pdfAsHtml/")
async def process_html(payload: HtmlPayload):
    print(f"Received HTML from {payload.url}")
    # Optional: Save or parse HTML
    global htmlPayload
    htmlPayload = payload 
    return {"status": "received", "length": len(payload.html)}




@app.post("/pdf_to_apl/")
async def pdf_to_apl(file: UploadFile = File(...), page_ignore: Optional[List[int]] = Form(None), encode: str = "utf8", save: str = None):
    """
    Converts the file to an APL and returns a cookie
    Parameters
    ----------
    file :
    page_ignore :
    encode :
    save :

    Returns
    -------

    """
    global apl_store

    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed."})

    file_bytes = await file.read()
    cpl = CompressedPostingsList(pymupdf.Document(stream=file_bytes))

    # Associate APL with cookie
    unique_key = str(uuid.uuid4())

    response = JSONResponse(content={"Process": "pdf to apl process completed"})
    response.set_cookie(key=unique_key)
    apl_store[unique_key] = cast(cpl, CompressedPostingsList)

    return {"response": response, "sid": unique_key} 

@app.get("/apl/command/{query}")
async def query_apl(query: str, session_id: Annotated[str | None, Cookie()] = None, CI_syn : float = 0.1, CI_sim : float = 0.7):
    """
    Execute a query on the APL. Uses cookies to differentiate between users
    Parameters
    ----------
    session_id :
    query :
    CI_syn :
    CI_sim :

    Returns
    -------

    """
    if not session_id in apl_store:
        raise HTTPException(status_code=403, detail="Invalid cookie.")

    results = apl_store[session_id].execute_query(query=query)
    return {results}
