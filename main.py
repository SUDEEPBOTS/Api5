import os
import yt_dlp
from flask import Flask, request, jsonify
import traceback # Error ki puri kundli nikalne ke liye

app = Flask(__name__)

@app.route('/')
def home():
    # Home page pe hi check kar lenge ki cookies hai ya nahi
    cookie_status = "✅ FOUND" if os.path.exists("cookies.txt") else "❌ MISSING"
    return f"API Status: ONLINE 🔥<br>Cookies File: {cookie_status}"

@app.route('/extract')
def extract():
    # 1. PRINT: Dekhte hain request mein kya aaya
    url = request.args.get('url')
    print(f"\n🔵 [NEW REQUEST] Aaya hua URL: {url}")
    
    if not url:
        print("🔴 ERROR: URL nahi mila request mein!")
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
    }

    # 2. PRINT: Cookies check
    if os.path.exists('cookies.txt'):
        print("🟢 INFO: Cookies file mil gayi, use kar raha hu.")
        ydl_opts['cookiefile'] = 'cookies.txt'
    else:
        print("jw WARNING: Cookies file nahi mili! Bina cookies ke try karunga.")

    try:
        print("🟡 STATUS: yt-dlp download start kar raha hai...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # 3. PRINT: Success hone par
            print(f"🟢 SUCCESS: Song mil gaya! Title: {info.get('title')}")
            
            return jsonify({
                "status": "success",
                "title": info.get('title'),
                "url": info.get('url'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail')
            })

    except Exception as e:
        # 4. PRINT: Agar fat gaya toh kyu fata?
        error_msg = str(e)
        full_traceback = traceback.format_exc()
        
        print(f"🔴 CRASH: Error aa gaya!")
        print(f"Error Message: {error_msg}")
        print(f"Full Details: {full_traceback}")
        
        return jsonify({"error": error_msg, "details": "Check Heroku Logs for full traceback"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    pp
