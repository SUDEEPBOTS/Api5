import os
import yt_dlp
from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    cookie_status = "✅ FOUND" if os.path.exists("cookies.txt") else "❌ MISSING"
    return f"API Status: ONLINE (Bot Friendly Mode) 🔥<br>Cookies File: {cookie_status}"

@app.route('/extract')
def extract():
    url = request.args.get('url')
    print(f"\n🔵 [RAW REQUEST] Bot ne bheja: {url}")
    
    if not url:
        return jsonify({"error": "No URL provided", "status": "false"}), 400

    # ==========================================
    # 🛠️ SMART FIXER
    # ==========================================
    if "/song/" in url:
        try:
            clean_id = url.split("/song/")[1].split("?")[0]
            url = f"https://www.youtube.com/watch?v={clean_id}"
            print(f"✨ [AUTO-FIX] URL badal diya gaya: {url}")
        except:
            pass
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
            
            # 👇 YAHAN FIX KIYA HAI 👇
            # 'True' (Boolean) hata kar "true" (String) kar diya
            return jsonify({
                "status": "true",             # String format taaki .lower() kaam kare
                "title": info.get('title'),
                "url": info.get('url'),
                "link": info.get('url'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail')
            })

    except Exception as e:
        error_msg = str(e)
        print(f"🔴 CRASH: {error_msg}")
        # Error me bhi string bhejenge
        return jsonify({"status": "false", "error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

