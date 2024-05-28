import concurrent.futures
import traceback
from autonode.clients.ocr import OCRClient
from autonode.logger.logger import logger


class OCRService:

    def __init__(self):
        self.ocr = OCRClient()

    def ocr_images_parallel(self, data):
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            executor.map(self.ocr_image, data)
        return data

    def ocr_image(self, data):
        try:
            ocred_result = self.ocr.get_parallel_text(data["cropped_image_path"])
            if ocred_result:
                all_text = self.concatenate_all_text(ocred_result).strip()
                if len(all_text) < 2:
                    data["ocr_result"] = None
                else:
                    data["ocr_result"] = all_text
            else:
                data["ocr_result"] = None
        except Exception as e:
            data["ocr_result"] = None
            logger.error(f"Error in ocr_image : {e}")

    def concatenate_all_text(self, ocred_data):
        text = ""
        for data in ocred_data:
            text += data["text"] + " "
        return text
