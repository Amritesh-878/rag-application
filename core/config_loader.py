import json
import os
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / '.env', override=True)

class Config:
    def __init__(self, config_path: str = "config.json"):
        if not os.path.isabs(config_path):
            project_root = Path(__file__).parent.parent
            config_file = project_root / config_path
        else:
            config_file = Path(config_path)
            
        if not config_file.exists():
            raise FileNotFoundError(f"Config file {config_file} not found")
        
        with open(config_file, 'r') as f:
            self.config = json.load(f)
    
    def get(self, key_path: str, default=None):
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_path(self, key_path: str) -> Path:
        path_str = self.get(key_path)
        if not path_str:
            raise ValueError(f"Path not found for {key_path}")
        return Path(path_str)
    
    @property
    def docs_dir(self) -> Path:
        return self.get_path('paths.docs_directory')
    
    @property
    def data_dir(self) -> Path:
        return self.get_path('paths.data_directory')
    
    @property
    def db_path(self) -> Path:
        return self.get_path('paths.db_path')
    
    @property
    def groq_api_key(self) -> str:
        key = os.getenv('GROQ_API_KEY')
        if not key or key == 'your_groq_api_key_here':
            raise ValueError("GROQ_API_KEY not set in environment variables")
        return key
    
    @property
    def unstructured_api_key(self) -> str:
        return os.getenv('UNSTRUCTURED_API_KEY', '')

config = Config()
