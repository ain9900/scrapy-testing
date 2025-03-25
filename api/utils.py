import subprocess
import uuid
import json

def run_scrapy_job(url):
    job_id = str(uuid.uuid4())
    output_file = f"output_{job_id}.json"
    subprocess.run([
        "scrapy", "crawl", "seo_spider",
        "-a", f"url={url}",
        "-o", output_file
    ])
    with open(output_file) as f:
        return json.load(f)
