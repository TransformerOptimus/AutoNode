import os
from autonode.models.files import Files
from autonode.utils.helpers.naming_helper import NamingHelper
from autonode.logger.logger import logger


class ScreenshotGenerator:

    def __init__(self):
        pass

    def run(self, db_session, s3_client, web_automator, step, request_id, request_dir, loop):
        screenshot_filename = NamingHelper.screenshot_file_name_generation(step)
        screenshot_filename = os.path.join(request_dir, screenshot_filename)
        loop.run_until_complete(web_automator.take_screenshot(screenshot_filename))

        # Uncomment If you have aws account and want to store result in your AWS S3
        # s3_client.upload_file(file_path=screenshot_filename)
        screenshot_store = Files.add_file(
            session=db_session,
            request_id=request_id,
            path=screenshot_filename,
            category="DEBUG",
            file_type="image",
            meta_data=None,
        )
        logger.info(f"Screenshot captured for request id {request_id} at step {step}")
        return screenshot_filename, screenshot_store.id
