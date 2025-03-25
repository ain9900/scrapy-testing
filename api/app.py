from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import uuid
import json
import os

app = Flask(__name__)
# Enable CORS for all routes with any origin
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/analyze/', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL in request"}), 400
    
    url = data['url']
    # Generate a unique job ID for the output file
    job_id = str(uuid.uuid4())
    output_file = f"output_{job_id}.json"
    
    try:
        # Run the Scrapy spider synchronously
        subprocess.run(
            ["scrapy", "crawl", "seo_spider", "-a", f"url={url}", "-o", output_file],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Scrapy error: {str(e)}"}), 500
    
    try:
        with open(output_file, "r") as f:
            result = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Error reading output file: {str(e)}"}), 500
    
    # Optionally, remove the output file after reading
    # os.remove(output_file)
    
    return jsonify({"message": "Analysis complete", "result": result})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

