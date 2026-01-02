import os
import yt_dlp
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    cookie_status = "✅ FOUND" if os.path.exists("cookies.txt") else "❌ MISSING"
    return f"API Status: ONLINE (Bot Friendly Mode - Trying 'ok') 🔥<br>Cookies File: {cookie_status}"

@app.route('/extract')
def extract():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided", "status": "fail"}), 400

    # SMART FIXER
    if "/song/" in url:
        try:
            clean_id = url.split("/song/")[1].split("?")[0]
            url = f"https://www.youtube.com/watch?v={clean_id}"
        except:
            pass
    elif "/video/" in url:
        try:
            clean_id = url.split("/video/")[1].split("?")[0]
            url = f"https://www.youtube.com/watch?v={clean_id}"
        except:
            pass

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # 👇 MAGIC FIX: "ok" status bhej rahe hain
            return jsonify({
                "status": "200",  
                "title": info.get('title'),
                "url": info.get('url'),
                "link": info.get('url'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail')
            })

    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
