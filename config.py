import yaml
import os
from pathlib import Path


class AppConfig:
    env = os.getenv("ENV")
    config_folder: str = "config"
    config_file: str = "parameters.yml" if env == "prd" else f"parameters_test.yml"

    @classmethod
    def load_config(cls):
        config_path = Path(cls.config_folder) / cls.config_file
        with open(config_path, "r") as f:
            return yaml.safe_load(f)


# Load the configuration
app_config = AppConfig()
parameter_config = app_config.load_config()
