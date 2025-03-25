from celery import Celery
import subprocess

# Set up the Celery app; using Redis as the broker.
app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task(bind=True)
def run_scraper(self, url):
    """
    This task runs your scraper for the given URL.
    It uses subprocess to call your Scrapy spider.
    """
    # You can generate a unique output file if needed
    output_file = f"output_{url.replace('https://','').replace('/','_')}.json"
    try:
        # Run the Scrapy spider; adjust the command as needed.
        subprocess.run([
            "scrapy", "crawl", "seo_spider",
            "-a", f"url={url}",
            "-o", output_file
        ], check=True)
        return {"url": url, "status": "completed", "output_file": output_file}
    except subprocess.CalledProcessError as e:
        # Optionally, retry or log errors here.
        self.retry(exc=e, countdown=10, max_retries=3)
