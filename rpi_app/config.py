import yaml

class Config:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def __getattr__(self, name):
        if name in self.config:
            return self.config[name]
        raise AttributeError(f"'Config' object has no attribute '{name}'")

    def __getitem__(self, item):
        return self.config.get(item, None)

# Usage example
config = Config('E:/basic_programming_workspace/python/project_raspberry/config.yml')

#folder-locations
video_folder = config.location['video_folder']
image_folder = config.location['image_folder']

#tcp
host = config.tcp['host']
port = config.tcp['port']

