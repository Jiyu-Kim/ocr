from PIL import Image
import cv2
import pytesseract
import json
from collections import defaultdict
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

class Tesseract:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    def recognize(self, image_path):
        # Open image
        image = Image.open(image_path)
        bounds = pytesseract.image_to_data(image, lang='kor+eng', output_type=pytesseract.Output.DICT)
        # Create json file
        data = []
        box_num = len(bounds['level'])
        for i in range(box_num):
            if(bounds['text'][i] != ""):
                #temp = defaultdict()
                temp = dict()
                text = bounds['text'][i]
                x = bounds['left'][i]
                y = bounds['top'][i]
                width = bounds['width'][i]
                height = bounds['height'][i]

                temp["text"] = text
                temp["x"] = x
                temp["y"] = y
                temp["width"] = width
                temp["height"] = height

                data.append(temp)

        #with open('data.json', "w", encoding="utf-8") as make_file:
            #json.dump(data, make_file, ensure_ascii=False, indent="\t", cls=NpEncoder)\
        return data