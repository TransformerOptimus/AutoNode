from yolo.yolo.services.model_service import ModelService
from yolo.yolo.utils.box_utils import process_bounding_boxes
from yolo.yolo.enums.model_type import ModelType
import io
from PIL import Image
import numpy as np


class YoloService:
    def __init__(self, model_type: ModelType = ModelType.SAHI):
        if model_type == ModelType.SAHI or model_type == ModelType.ULTRALYTICS:
            self.model_type = model_type
        else:
            raise Exception('No Model is configured. Please configure')

    def detect(self, image_contents: bytes) -> list:
        image_obj = Image.open(io.BytesIO(image_contents)).convert("RGB")
        boxes, bbox_class_name = ModelService(model_type=self.model_type).predict(image_obj, image_contents)
        return process_bounding_boxes(self.model_type, boxes, bbox_class_name)
