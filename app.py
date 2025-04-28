from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
import requests

app = Flask(__name__)

# Setup your proxy config
PROXY = {
    "http": "http://broqhspi:y42o6io2umet@38.153.152.244:9594",
    "https": "http://broqhspi:y42o6io2umet@38.153.152.244:9594"
}



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    video_url = data.get('url')
    video_id = extract_video_id(video_url)
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(
            video_id,
            proxies=PROXY  # Pass the proxy here
        )
        full_text = "\n".join(item['text'] for item in transcript_data)
        return jsonify({'transcript': full_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def extract_video_id(url):
    import re
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

if __name__ == '__main__':
    app.run(debug=True)
