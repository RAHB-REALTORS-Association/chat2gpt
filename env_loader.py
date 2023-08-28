import os
from dotenv import load_dotenv
from settings import SETTINGS

load_dotenv()  # This will load environment variables from a .env file if it exists

class EnvironmentLoader:
    def __init__(self):
        self.loaded_envs = {}  # Initialize the attribute as an empty dictionary
        
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvironmentLoader, cls).__new__(cls)
            cls._instance.loaded_envs = {}
            cls._instance.load_environment()  # Loading environment variables during instantiation
        return cls._instance

    def load_environment(self):
        for env_name, env_details in SETTINGS.items():
            value = os.getenv(env_name, env_details.get("default"))

            # If required and not provided, raise an exception
            if env_details.get("required") and value is None:
                raise ValueError(f"{env_name} environment variable is required and not set.")

            # Convert to appropriate data type if needed
            if value is not None:
                value = env_details["type"](value)

            self.loaded_envs[env_name] = value

    def get(self, key):
        return self.loaded_envs.get(key, None)

# Singleton instance
_env_loader_instance = EnvironmentLoader()

# Global function to get environment variable
def get_env(key):
    return _env_loader_instance.get(key)
