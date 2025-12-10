from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import traceback

app = Flask(__name__)

class YTDLPLogger:
    def debug(self, msg):
        print("[DEBUG]", msg)

    def warning(self, msg):
        print("[WARNING]", msg)

    def error(self, msg):
        print("[ERROR]", msg)


@app.route("/extract", methods=["GET"])
def extract():
    url = request.args.get("url")

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    print(f"📥 Received request: {url}")

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": False,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "extract_flat": False,
        "logger": YTDLPLogger(),
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9",
        }
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info.get("url")

            print(f"✅ Extracted audio URL: {audio_url}")

            return jsonify({
                "status": "success",
                "audio_url": audio_url,
                "title": info.get("title")
            })

    except Exception as e:
        print("🔥 ERROR OCCURRED IN /extract")
        print(traceback.format_exc())  # يطبع الخطأ بالكامل في Render log

        return jsonify({
            "status": "error",
            "message": str(e),
            "details": traceback.format_exc(),
        }), 500


if __name__ == "__main__":
    print("🚀 Server Started on port 10000")
    app.run(host="0.0.0.0", port=10000)
