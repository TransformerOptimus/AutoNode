import uuid
from yolo.yolo.enums.model_type import ModelType


def process_bounding_boxes(model_type, boxes, bbox_class_name):
    if model_type == ModelType.SAHI:
        return _process_sahi_bounding_boxes(boxes)
    else:
        return _process_other_bounding_boxes(boxes, bbox_class_name)


def _process_sahi_bounding_boxes(boxes):
    """
        Function to process the bounding boxes to get the points

        Args:
            boxes (Box): sahi box object

        Returns:
            List: list of points
    """

    points = []
    for box in boxes:
        x1, y1, w, h = box['bbox']
        points.append({
            "bbox": [float(x1), float(y1), float(x1 + w), float(y1 + h)],
            "class": box['category_name'],
            "id": str(uuid.uuid4())
        })
    return points


def _process_other_bounding_boxes(boxes, bbox_class_name):
    """
        Function to process the bounding boxes to get the points

        Args:
            boxes (Box): ultralytics box object
            bbox_class_name (str)

        Returns:
            List: list of points
    """
    points = []

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        predicted_class = box.cls[0]
        points.append({
            "bbox": [float(x1), float(y1), float(x2), float(y2)],
            "class": bbox_class_name[int(predicted_class)],
            "id": str(uuid.uuid4())
        })
    return points
