import os
from dotenv import load_dotenv
from openai import OpenAI


class Settings:
    """
    Configuration class for managing settings.

    Attributes:
        debug (bool): Flag indicating whether debug mode is enabled.
        openai_api_key (str): API key for OpenAI.
        google_api_key (str): API key for Google.
        monitor_size (dict): Dictionary containing the width and height of the monitor.
    """

    def __init__(self):
        load_dotenv()
        self.debug = False
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.monitor_size = {
            "width": 1920,
            "height": 1080,
        }
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_URL = f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:5432/{self.DB_NAME}"

        self.db_engine_args = {
            "pool_size": 20,  # Maximum number of database connections in the pool
            "max_overflow": 50,  # Maximum number of connections that can be created beyond the pool_size
            "pool_timeout": 30,  # Timeout value in seconds for acquiring a connection from the pool
            "pool_recycle": 1800,  # Recycle connections after this number of seconds (optional)
            "pool_pre_ping": False,  # Enable connection health checks (optional)
        }
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("BUCKET_NAME") if os.getenv("BUCKET_NAME") else "autonode-jobs"

    def initialize_openai_client(self):
        """
        Initializes and returns an OpenAI client with the configured API key.

        Returns:
            OpenAI or None: An instance of the OpenAI client if the API key is provided, else None.
        """
        if self.openai_api_key:
            client = OpenAI()
            client.api_key = self.openai_api_key
            client.base_url = os.getenv("OPENAI_API_BASE_URL", client.base_url)
            return client
        return None
