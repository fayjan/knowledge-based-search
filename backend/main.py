from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from .engine import RAGEngine

app = FastAPI(title="Knowledge Based Search API")
engine = RAGEngine()

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SearchQuery(BaseModel):
    query: str

@app.post("/ingest")
async def process_files(files: list[UploadFile] = File(...)):
    paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        paths.append(file_path)
    
    engine.ingest_docs(paths)
    return {"message": f"Successfully indexed {len(files)} files."}

@app.post("/search")
async def search(data: SearchQuery):
    answer = engine.query_knowledge_base(data.query)
    return {"answer": answer}