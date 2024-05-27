import json
import os
from typing import Dict
from pathlib import Path


class KafkaConfigLoader:
    def __init__(self):
        self.config_path = self._determine_config_path()

    def _determine_config_path(self) -> Path:
        env = os.getenv('APP_ENV', 'development').lower()  # Default to 'development' if unset
        current_dir = Path(__file__).parent
        config_filename = f"kafka_config_{env}.json"
        return current_dir / config_filename

    def load_config(self) -> Dict[str, str]:
        try:
            with open(self.config_path, 'r') as config_file:
                config = json.load(config_file)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Kafka configuration file not found at {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in Kafka configuration file")
