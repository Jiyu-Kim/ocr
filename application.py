import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from EasyOCR import EasyOCR
from Tesseract import  Tesseract

root_path ="C:/Users/SoftCamp/Desktop/ocr/static"
app = Flask(__name__)

# 파일 업로드 처리
@app.route("/", methods=["POST", "GET"])
def index():
    text_detected = "This is text."
    return render_template("index.html", text_detected = text_detected)

@app.route("/fileupload", methods=['POST'])
def file_upload():
    if request.method == 'POST':
        # receive image file
        file = request.files['file']
        filename = secure_filename(file.filename)
        # save image file
        os.makedirs(root_path, exist_ok=True)
        image_path = os.path.join(root_path, filename)
        file.save(image_path)
        # detect text from image
        ocr_engine = EasyOCR()
        bounds = ocr_engine.recognize(image_path)
        text = []
        for bound in bounds:
            text.append(bound['text'])
        
    return render_template("output.html", text=text)

if __name__ == "__main__":
    app.run(port="5000", debug=True, host="0.0.0.0")