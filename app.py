from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    path = './downloads'

    if not url:
        return jsonify({'status': 'error', 'message': 'Missing YouTube URL'}), 400

    try:
        os.makedirs(path, exist_ok=True)
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        output_file = stream.download(output_path=path)
        return jsonify({'status': 'success', 'file_path': output_file})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
