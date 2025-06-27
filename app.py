from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "YouTube Downloader API is running!"

@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(output_path="/tmp")
        return jsonify({"message": "Video downloaded successfully", "title": yt.title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
