import os

from dotenv import load_dotenv

load_dotenv()


class OcrConfig:
    environment = os.getenv('APP_ENV', 'DEV').upper()
    gpu = os.getenv('OCR_GPU', 'TRUE') == 'TRUE'
    languages = os.getenv('OCR_LANGUAGES', 'en').split(',')

    use_remote_service = os.getenv('USE_REMOTE_OCR', False)
    ocr_remote_url = os.getenv('OCR_REMOTE_URL', '<OCR_REMOTE_URL>')

    base_image_path = os.getenv('BASE_IMAGE_PATH', 'gpu_service_images/')
    easyocr_image_decoder = os.getenv('EASYOCR_IMAGE_DECODER', 'beamsearch')
    easyocr_text_threshold = os.getenv('EASYOCR_TEXT_THRESHOLD', 0.4)
    easyocr_image_decoder_beam_width = int(os.getenv('EASYOCR_IMAGE_DECODER_BEAM_WIDTH', 10))
    easyocr_image_decoder_width_ths = float(os.getenv('EASYOCR_IMAGE_DECODER_WIDTH_THS', 0.3))
    easyocr_image_decoder_batch_size = int(os.getenv('EASYOCR_IMAGE_DECODER_BATCH_SIZE', 10))
    easyocr_image_decoder_mag_ratio = int(os.getenv('EASYOCR_IMAGE_DECODER_MAG_RATIO', 3))
    easyocr_image_decoder_low_text = float(os.getenv('EASYOCR_IMAGE_DECODER_LOW_TEXT', 0.4))
