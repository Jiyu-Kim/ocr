from PIL import Image
import easyocr
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

class EasyOCR:
    def __init__(self):
        #self.reader = easyocr.Reader(['ko', 'en'], gpu=False)
        self.reader = easyocr.Reader(['ko', 'en'])
        
    def recognize(self, image_path):
        # Open image
        image = Image.open(image_path)

        # Get text detected and bounding boxes
        bounds = self.reader.readtext(image)

        # Create json file
        data = []
        for bound in bounds:
            #temp = defaultdict()
            temp = dict()
            text = bound[1]
            top_left = bound[0][0] # [([top_left, top_right, botton_right, bottom_left], text_detacted, confident_level)]
            bottom_right = bound[0][2]
            x = top_left[0]
            y = top_left[1]
            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]

            temp["text"] = text
            temp["x"] = x
            temp["y"] = y
            temp["width"] = width
            temp["height"] = height
            
            data.append(temp)
            
        #with open('data.json', "w", encoding="utf-8") as make_file:
            #json.dump(data, make_file, ensure_ascii=False, indent="\t", cls=NpEncoder)
        
        return data