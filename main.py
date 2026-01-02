import os
import yt_dlp
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Tera Bhai Ka API Mast Chal Raha Hai (With Local Cookies)! 🔥"

@app.route('/extract')
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Ab ye seedha 'cookies.txt' file uthayega root folder se
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt',  # Direct file path
        'geo_bypass': True,
    }

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
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
