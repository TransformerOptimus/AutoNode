import os

from dotenv import load_dotenv

load_dotenv()


class YoloConfig:
    environment = os.getenv('APP_ENV', 'DEV').upper()

    use_remote_service = os.getenv('USE_REMOTE_YOLO', False)
    yolo_remote_url = os.getenv('YOLO_REMOTE_URL', '<YOLO_REMOTE_URL>')

    sahi_model_type = os.getenv('SAHI_MODEL_TYPE', 'yolov8')
    sahi_model_path = os.getenv('SAHI_MODEL_PATH', 'yolo/web_detection_models/apollo.pt')
    sahi_confidence_threshold = float(os.getenv('SAHI_CONFIDENCE_THRESHOLD', '0.2'))
    sahi_slice_width = int(os.getenv('SAHI_SLICE_WIDTH', '1280'))
    sahi_slice_height = int(os.getenv('SAHI_SLICE_HEIGHT', '710'))
    sahi_overlap_height_ratio = float(os.getenv('SAHI_OVERLAP_HEIGHT_RATIO', '0.2'))
    sahi_overlap_width_ratio = float(os.getenv('SAHI_OVERLAP_WIDTH_RATIO', '0.2'))
    sahi_export_dir = os.getenv('SAHI_EXPORT_DIR', 'runs/detect/')
    ultralytics_model_path = os.getenv('ULTRALYTICS_MODEL_PATH', 'yolo/web_detection_models/apollo.pt')
    ultralytics_confidence_threshold = float(os.getenv('ULTRALYTICS_CONFIDENCE_THRESHOLD', '0.2'))
    ultralytics_save = os.getenv('ULTRALYTICS_SAVE', 'TRUE') == 'TRUE'
