import uuid

from anyio import TemporaryFile
from fastapi import FastAPI, File, UploadFile, Form, Cookie, Response, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from pdfwordsearch.match_score_rank.execute_query import execute_query
from typing import List, Optional, Annotated, Dict, cast
from pdfwordsearch.scan.pdf_scan import pdf_info_get
from pdfwordsearch.scan.pdf_to_pl import pdf_to_pl

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Storage (RAM for now but can be changed to disk storage later)
apl_store : Dict[Cookie, CompressedPostingsList] = dict()


@app.post("/pdf_to_apl/")
async def pdfToApl(response: Response, file: UploadFile = File(...), page_ignore: Optional[List[int]] = Form(None), encode: str = "utf8", save: str = None):
    """
    Converts the file to an APL and returns a cookie
    Parameters
    ----------
    response :
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

    ## process 1: obtaining the abstract table:
    fl = pdf_info_get(file.file, ignore_page=page_ignore, encode=encode, save=save, is_binary=True)
    ## process 2: convert to compressed posting list
    apl = pdf_to_pl(fl, CompressedPostingsList)

    # Associate APL with cookie
    unique_key = str(uuid.uuid4())

    response.set_cookie(key=unique_key)
    apl_store[unique_key] = cast(apl, CompressedPostingsList)

    return {"Process": "pdf to apl process completed"}

@app.get("/apl/command/{query}")
async def query_apl(query: str, cookie : Annotated[str | None, Cookie()] = None, CI_syn : float = 0.1, CI_sim : float = 0.7):
    """
    Execute a query on the APL. Uses cookies to differentiate between users
    Parameters
    ----------
    query :
    cookie :
    CI_syn :
    CI_sim :

    Returns
    -------

    """
    if not cookie in apl_store:
        raise HTTPException(status_code=403, detail="Invalid cookie.")

    results = execute_query(query=query, postings_list=apl_store[cookie])
    return {results}
