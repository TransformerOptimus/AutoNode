import os
import shutil
import string
import re


class CleanupHelper:

    def __init__(self):
        pass

    @classmethod
    def clear_folders(cls, folders: [str]):
        """Function to clear the cropped images folders
        """
        for folder in folders:
            try:
                shutil.rmtree(folder)

            except Exception as e:
                raise e

            finally:
                os.makedirs(folder)

        return True

    @classmethod
    def clean_response(cls, response: str) -> str:
        response = ''.join(char for char in response if char in string.printable)
        if response.startswith("```json") and response.endswith("```"):
            response = "```json".join(response.split("```")[1:-1])
            response = re.sub(r"\bjson\b", "", response)

        elif response.startswith("```") and response.endswith("```"):
            response = "```".join(response.split("```")[1:-1])
            response = re.sub(r"\bjson\b", "", response)
        return response

    @classmethod
    def type_response_cleaner(cls, response):
        return cls._remove_quotes(response)

    @classmethod
    def _remove_quotes(cls, response):
        return re.sub(r'["\']', '', response)
