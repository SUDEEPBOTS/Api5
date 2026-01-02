import os
import yt_dlp
from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    cookie_status = "✅ FOUND" if os.path.exists("cookies.txt") else "❌ MISSING"
    return f"API Status: ONLINE 🔥<br>Cookies File: {cookie_status}"

@app.route('/extract')
def extract():
    url = request.args.get('url')
    print(f"\n🔵 [RAW REQUEST] Bot ne bheja: {url}")
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # ==========================================
    # 🛠️ SMART FIXER (Ye naya code hai)
    # ==========================================
    # Agar bot "/song/ID" bhej raha hai, toh hum usse asli link banayenge
    if "/song/" in url:
        try:
            # "/song/" ke baad wala hissa (Video ID) nikaalo
            # Example: /song/LV_wiOhO40Q?api=None -> LV_wiOhO40Q
            clean_id = url.split("/song/")[1].split("?")[0]
            
            # Asli YouTube Link banao
            url = f"https://www.youtube.com/watch?v={clean_id}"
            print(f"✨ [AUTO-FIX] URL badal diya gaya: {url}")
        except Exception as e:
            print(f"⚠️ URL fix karne me dikkat aayi: {e}")

    # Agar bot "/video/" bhej raha hai (Video play ke liye)
    elif "/video/" in url:
        try:
            clean_id = url.split("/video/")[1].split("?")[0]
            url = f"https://www.youtube.com/watch?v={clean_id}"
            print(f"✨ [AUTO-FIX] Video URL badal diya gaya: {url}")
        except:
            pass
    # ==========================================

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
    }

    if os.path.exists('cookies.txt'):
        print("🟢 INFO: Cookies file mil gayi.")
        ydl_opts['cookiefile'] = 'cookies.txt'
    else:
        print("jw WARNING: Cookies file nahi mili!")

    try:
        print(f"🟡 STATUS: Downloading metadata for: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"🟢 SUCCESS: Title mil gaya -> {info.get('title')}")
            
            return jsonify({
                "status": "success",
                "title": info.get('title'),
                "url": info.get('url'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail')
            })

    except Exception as e:
        error_msg = str(e)
        print(f"🔴 CRASH: {error_msg}")
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
