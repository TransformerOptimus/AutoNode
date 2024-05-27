import os
from PIL import Image
import concurrent.futures
from autonode.logger.logger import logger


class ImageHelper:

    def __init__(self):
        pass

    def crop_images_parallel(self, image_path, results, folder_path):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for result in results:
                future = executor.submit(self.crop_image, image_path, result, folder_path)
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                except Exception as e:
                    logger.error(f"Error occurred during cropping: {e}")

        return results

    def crop_image(self, image_path, result, folder_path):
        try:
            image = Image.open(image_path)
            x1, y1, x2, y2 = result["bbox"]
            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_image_path = os.path.join(folder_path, f"cropped_image_{result['id']}.png")
            cropped_image.save(cropped_image_path)
            result["cropped_image_path"] = cropped_image_path
        except Exception as e:
            result["cropped_image_path"] = None
            logger.error(f"Error while cropping image: {e}")

        return result
