import base64

import requests
from PIL import Image
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
from ultralytics import YOLO
from yolo.yolo.configs.settings import YoloConfig as config
from yolo.yolo.enums.model_type import ModelType
from numpy import asarray


class ModelService:
    def __init__(self, model_type: ModelType):
        self.use_remote = config.use_remote_service
        self.model_type = model_type
        if self.model_type == ModelType.SAHI:
            self.model = AutoDetectionModel.from_pretrained(
                model_type=config.sahi_model_type,
                model_path=config.sahi_model_path,
                confidence_threshold=config.sahi_confidence_threshold,
            )
        elif self.model_type == ModelType.ULTRALYTICS:
            self.model = YOLO(config.ultralytics_model_path)
        else:
            raise Exception('One model must be specified that is either sahi or ultralytics.')

    def predict(self, image: Image, image_contents: bytes):
        if self.use_remote:
            return self._remote_predict(image_contents)
        else:
            return self.__predict(image)

    def __predict(self, image: Image):
        """
            Function to predict the bounding boxes of the image
            Args:
                image (Image): Image Object.
            Returns:
                Box: box object
        """
        if self.model_type == ModelType.SAHI:
            return self.__predict_sahi(image)
        elif self.model_type == ModelType.ULTRALYTICS:
            return self.__predict_ultralytics(image)
        else:
            raise Exception("Yolo Model not configured. Please configure")

    def __predict_sahi(self, image):
        results = get_sliced_prediction(image=image, detection_model=self.model,
                                        slice_width=config.sahi_slice_width, slice_height=config.sahi_slice_height,
                                        overlap_height_ratio=config.sahi_overlap_height_ratio,
                                        overlap_width_ratio=config.sahi_overlap_width_ratio)
        results.export_visuals(export_dir=config.sahi_export_dir)
        object_prediction_list = results.to_coco_annotations()
        return object_prediction_list, None

    def __predict_ultralytics(self, image):
        results = self.model.predict(
            source=asarray(image),
            conf=config.ultralytics_confidence_threshold,
            save=config.ultralytics_save
        )
        boxes = results[0].boxes.cpu().numpy()
        bbox_class_names = results[0].names

        return boxes, bbox_class_names

    def _remote_predict(self, image: bytes):
        print("Remote Prediction")
        """Function to predict the bounding boxes of the  from a remote gpu service

        Args:
            image (str): image for prediction

        Returns:
            Box: ultralytics box object
        """

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        image_base64 = self._image_to_base64(image)

        payload = {
            'data': image_base64
        }

        response = requests.post(config.yolo_remote_url, headers=headers, json=payload)
        result = response.json()
        print(f"Remote Prediction {result}")
        return result['received_data']

    def _image_to_base64(self, image):
        return base64.b64encode(image).decode('utf-8')

