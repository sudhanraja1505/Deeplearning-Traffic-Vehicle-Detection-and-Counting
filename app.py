import os
import uuid
from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from detector import process_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        uploaded = request.files.get("video")
        if not uploaded or uploaded.filename == "":
            error = "Please choose a video file."
        elif not allowed_file(uploaded.filename):
            error = "Unsupported file type. Upload MP4, AVI, MOV, or MKV."
        else:
            unique_id = uuid.uuid4().hex[:8]
            input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{secure_filename(uploaded.filename)}")
            output_name = f"processed_{unique_id}.mp4"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)
            uploaded.save(input_path)
            try:
                stats = process_video(input_path, output_path)
                result = {
                    "video_url": url_for("output_file", filename=output_name),
                    "total": stats["total"],
                    "counts": stats["counts"],
                    "frames": stats["frames"],
                }
            except Exception as exc:
                error = f"Could not process the video: {exc}"
            finally:
                try:
                    os.remove(input_path)
                except OSError:
                    pass
    return render_template("index.html", result=result, error=error)


@app.route("/outputs/<path:filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True)
