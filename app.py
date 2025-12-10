from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

def extract_best_audio(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestaudio/best",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_format = info.get("url")
        title = info.get("title") or "audio"
        # استبدال الأحرف غير الصالحة في اسم الملف
        safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
        return {
            "title": safe_title,
            "audio_url": audio_format
        }

@app.route("/extract", methods=["GET"])
def extract():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Parameter 'url' is required"}), 400

    try:
        result = extract_best_audio(url)
        if not result["audio_url"]:
            return jsonify({"error": "لم يتم العثور على رابط صوتي صالح"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
