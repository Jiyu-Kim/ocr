import os
from unicodedata import east_asian_width
from flask import Flask, render_template, request, make_response
from werkzeug.utils import secure_filename
from EasyOCR import EasyOCR
from Tesseract import  Tesseract

# load ocr engines
easyocr = EasyOCR()
tesseract = Tesseract()
engine_group = {"easyocr": easyocr, "tesseract": tesseract}

# root path where received image is saved
root_path ="C:/Users/SoftCamp/Desktop/ocr/static"

# allowed file extensions
allowed_types = ['png', 'jpg']

app = Flask(__name__)

# 파일 업로드 처리
@app.route("/", methods=["POST", "GET"])
def index():
    engine_types = []
    for engine_type in engine_group.keys():
        engine_types.append(engine_type)

    return render_template("index.html", engine_types=engine_types)

@app.route("/fileupload", methods=['POST'])
def file_upload():
    if request.method == 'POST':
        # recevie engine type
        engine_type = request.form['engine']

        # receive an image file
        file = request.files['file']
        filename = secure_filename(file.filename)

        # check whether received file is an image
        extension = filename.split('.')[1]
        if extension not in allowed_types:
            return make_response("Please Enter an Image file", 405)

        # save image file
        os.makedirs(root_path, exist_ok=True)
        image_path = os.path.join(root_path, filename)
        file.save(image_path)
        
        # detect text from image
        ocr_engine = engine_group[engine_type]
        bounds = ocr_engine.recognize(image_path)
        text = []
        for bound in bounds:
            text.append(bound['text'])
        
        return render_template("output.html", text=text)

if __name__ == "__main__":
    app.run(port="5000", debug=True, host="0.0.0.0")