from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from tasks import run_crawl_task
from database import SessionLocal
from models import AnalysisResult

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.post("/analyze/")
def analyze_url(request: URLRequest):
    task = run_crawl_task.delay(request.url)
    return {"message": "Task started", "task_id": task.id}

@app.get("/result/{task_id}")
def get_result(task_id: str):
    db = SessionLocal()
    result = db.query(AnalysisResult).filter(AnalysisResult.task_id == task_id).first()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return {"url": result.url, "data": result.data}
