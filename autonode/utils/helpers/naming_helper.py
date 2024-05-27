import uuid


class NamingHelper:

    @classmethod
    def screenshot_file_name_generation(cls, screenshot_idx: int) -> str:
        """
        Generate a screenshot file name.
        """
        return f"screenshot_{screenshot_idx}_{str(uuid.uuid4())}.png"

    @classmethod
    def screenshot_folder_name_generator(cls) -> str:
        """
        Generate a screenshot folder name.
        """
        return f"jobs_{str(uuid.uuid4())}"

    @classmethod
    def request_folder_name_generator(cls) -> str:
        """
        Generate a request folder name.
        """
        return f"req_{str(uuid.uuid4())}"
