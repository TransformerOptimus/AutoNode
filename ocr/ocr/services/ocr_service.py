import base64
from typing import List
import requests
from ocr.ocr.configs.settings import OcrConfig
from ocr.ocr.services.easy_ocr import EasyOcr
from ocr.ocr.utils.box_utils import convert_units_of_bbox, get_point
import io
from PIL import Image


class OcrService:
    def __init__(self, lang_list: List[str] = OcrConfig.languages, gpu: bool = OcrConfig.gpu):
        self.image = None
        self.use_remote = OcrConfig.use_remote_service
        self.lang_list = lang_list
        self.gpu = gpu

    def get_para_text(self, image: str) -> list:
        if self.use_remote:
            result_array = self._remote_predict(image)
        else:
            result_array = self._do_ocr(image)
        print(f"OCR Result for {image} {result_array} using remote {self.use_remote}")
        data = []
        for bbox, text in result_array:
            new_bbox = convert_units_of_bbox(bbox, self.image)
            point = get_point(new_bbox)
            data.append({'bbox': new_bbox, 'point': point, 'text': text})
        return data

    def get_text(self, image_contents: bytes) -> list:
        image_obj = Image.open(io.BytesIO(image_contents))
        result_array = EasyOcr(self.lang_list, self.gpu).predict_text(image_contents)
        # convert the units of the bounding box from easyocr to percentages from left and right
        data = []
        for bbox, text, prob in result_array:
            new_bbox = convert_units_of_bbox(bbox, image_obj)
            point = get_point(new_bbox)
            data.append({'bbox': new_bbox, 'point': point, 'text': text, 'prob': prob})
        return data

    def _remote_predict(self, image):
        self.image = self._read_image_object(image)
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        image_base64 = self._image_to_base64(image)

        payload = {
            'data': image_base64
        }

        response = requests.post(OcrConfig.ocr_remote_url, headers=headers, json=payload)
        result = response.json()
        return result['results']

    def _do_ocr(self, image_path):
        self.image = self._read_image_object(image_path)
        result = EasyOcr(self.lang_list, self.gpu).predict_para_text(image_path)
        return result

    def _read_image_object(self, path):
        return Image.open(path)

    def _image_to_base64(self, image_path):
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
