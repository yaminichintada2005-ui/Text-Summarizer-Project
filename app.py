from flask import Flask, render_template, request
import os

from summarizer.summarize import summarize_text
from summarizer.file_reader import read_text_file, read_pdf

UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = ""
    summary = ""

    if request.method == "POST":
        # 1️⃣ Get manual text
        input_text = request.form.get("input_text", "").strip()

        # 2️⃣ Get file
        file = request.files.get("file")

        if input_text:
            extracted_text = input_text

        elif file and file.filename:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            if file.filename.endswith(".txt"):
                extracted_text = read_text_file(filepath)

            elif file.filename.endswith(".pdf"):
                extracted_text = read_pdf(filepath)

        if extracted_text:
            summary = summarize_text(extracted_text)

    return render_template(
        "index.html",
        extracted_text=extracted_text,
        summary=summary
    )
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
