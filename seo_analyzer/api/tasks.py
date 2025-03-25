from celery import Celery
from utils import run_scrapy_job

app = Celery("tasks", broker="redis://redis:6379/0")

@app.task(bind=True)
def run_crawl_task(self, url):
    result_data = run_scrapy_job(url)
    from database import SessionLocal
    from models import AnalysisResult
    db = SessionLocal()
    db_result = AnalysisResult(url=url, task_id=self.request.id, data=result_data)
    db.add(db_result)
    db.commit()
    db.close()
