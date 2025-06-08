from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
import os
from pdfwordsearch.scan import pdf_info_get, pdf_to_APL
from typing import List, Optional
from pdfwordsearch.match import search_posting_list

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Storage (RAM for now but can be changed to disk storage later)
apl_store = None


@app.post("/pdf_to_apl/")
async def pdfToApl(file: UploadFile = File(...), page_ignore: Optional[List[int]] = Form(None), encode: str = "utf8", save: str = None):
    global apl_store
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files are allowed."})

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ## process 1: obtaining the abstract table:
    fl = pdf_info_get(file_path, ignorePage=page_ignore, encode=encode, save=save)
    ## process 2: convert to compressed posting list
    apl = pdf_to_APL(fl)

    # now apl is the CompressedPostingsList object 
    apl_store = apl  # Store the apl in memory 

    return {"Process": "pdf to apl process completed"}


@app.get("/apl/{word}")
async def search_apl(word: str, CI_syn : float = 0.3, CI_sim : float = 0.9):
    """Search for a word in the stored APL."""
    return search_posting_list(word, apl_store, CI_syn, CI_sim)

@app.get("/apl/command/{command}")
async def command_apl(command: str, CI_syn : float = 0.1, CI_sim : float = 0.7):
    """Execute a command on the stored APL."""
    """ 
    Some sort of the command (unsure what is this for now)
    like?:
    lovely & (power | strange)  
    as example? 
        
    """
    # tbd 
    return {"command": command }
