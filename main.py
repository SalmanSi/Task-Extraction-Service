import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
from services.milestone_service import analyze_milestones

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development; you can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Ensure allowed file types
    allowed_exts = [".pdf", ".txt", ".docx"]
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_exts:
        logger.warning(f"Unsupported file type upload attempt: {file.filename}")
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    # Save uploaded file
    saved_path = DOCUMENTS_DIR / file.filename
    # if saved_path.exists():
    #     raise HTTPException(status_code=400, detail="File with this name already exists.")
    with open(saved_path, "wb") as buffer:
        buffer.write(await file.read())
    logger.info(f"File saved: {saved_path}")

    # Run milestone analysis
    try:
        logger.info(f"Starting milestone analysis on: {saved_path}")
        result = analyze_milestones(str(saved_path), provider="openai")  # or "gemini"
        logger.info(f"Milestone analysis completed for: {saved_path}")
        logger.info(f"LLM response: {result.model_dump()}")
    except Exception as e:
        logger.exception(f"Error during milestone analysis for {saved_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content=result.model_dump())
