import os
import shutil
import json
from fastapi import FastAPI, File, UploadFile, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .models import Job
from .database import get_db, init_db
from . import processing

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/process/{job_id}")
async def process_job(job_id: str, background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        return {"error": "Job not found"}

    # Save uploaded file
    file_path = f"/data/raw/{job_id}/images/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update job status
    job.status = "processing"
    db.commit()

    # Process images in the background
    background_tasks.add_task(process_and_update_job, job_id, db)

    return {"message": "Job queued for processing"}

@app.get("/job/{job_id}")
async def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        return {"error": "Job not found"}

    # If job is completed, include the Potree URL
    if job.status == "completed":
        metadata_file = f"/data/processed/{job_id}/metadata.json"
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            job.potree_url = metadata.get("potree_url")

    return job

def process_and_update_job(job_id: str, db: Session):
    try:
        processing.process_images(job_id)
        
        # Update job status
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "completed"
        db.commit()
    except Exception as e:
        # Update job status to failed
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "failed"
        job.error_message = str(e)
        db.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)