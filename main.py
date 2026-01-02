import os
import yt_dlp
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # Ye check karega ki file server pe pahunchi ya nahi
    if os.path.exists("cookies.txt"):
        return "API Running 🔥 | Cookies File: FOUND ✅"
    else:
        return "API Running 🔥 | Cookies File: NOT FOUND ❌ (Upload kar bhai)"

@app.route('/extract')
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Options setup
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
    }

    # IMPORTANT: Check karega file hai ya nahi
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
    else:
        print("WARNING: cookies.txt file nahi mili! Bina cookies ke try kar raha hu.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "success",
                "title": info.get('title'),
                "url": info.get('url'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        # Error ko print karega logs me taaki hum dekh sakein
        print(f"Extraction Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
