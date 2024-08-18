import json
import os

class Config:
    def __init__(self, config_file="chat_config.json"):
        self.config_file = config_file
        self.system_prompt = "You are a helpful AI assistant."
        self.model = "claude-3-opus-20240229"
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.system_prompt = config.get('system_prompt', self.system_prompt)
                self.model = config.get('model', self.model)
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump({
                'system_prompt': self.system_prompt,
                'model': self.model
            }, f)
