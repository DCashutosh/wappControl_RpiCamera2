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
config = Config('E:/basic_programming_workspace/python/project_local/config.yml')

#whatsapp-configs
def_sender = config.whatsapp['def_sender']
url = config.whatsapp['url']

#system-chats
def_msg = config.whatsapp['def_msg']
instruction = config.whatsapp['instruction']

#selenium-configs
exec_path = config.selenium['exec_path']
profile_path = config.selenium['profile_path']
profile = config.selenium['browser_profile']

#whatsapp-xpaths
link_mobile = config.xpaths['link_mobile']
sender_box = config.xpaths['sender_box']
code_box = config.xpaths['code_box']
contact_search = config.xpaths['search_box']
message_box = config.xpaths['message_box']
msg_tymstamp = config.xpaths['recent_msg_timestamp']
attach_file = config.xpaths['attach_file']
select_file = config.xpaths['select_file']
file_send = config.xpaths['file_send']
# print("The default sender is : "+def_sender)
# print(def_msg)

#folder-locations
video_folder = config.location['video_folder']
image_folder = config.location['image_folder']

#netwrok
host = config.network['host']
port = config.network['port']
