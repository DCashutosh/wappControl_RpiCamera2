from wapp_init import Wapp_init
from wapp_apps import Wapp_apps
# from cameraController import CameraController
# from servoController import ServoController
# from osController import OsController
from serverClient import ServerClient

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import config as Config
import time as time
import re

#user-setup
user = input("Please provide the user(Contact) : ")

if(user.startswith("+1")):
    formatted_user = f"{user[:2]}({user[2:5]}){user[5:8]}-{user[8:]}"
elif(user.startswith("+91")):
    formatted_user = f"{user[:3]} {user[3:8]} {user[8:]}"

# print(formatted_user)
# cameraControl = CameraController()
# servoControl = ServoController()
# osControl = OsController()
sClient = ServerClient()


def processRequest(apps,cmd, img_counter, vdo_counter):
    # msg = "Processing Request !!!"
    apps.send_msg("Processing Request !!!")

    if(cmd == "instashot"):
        
        file_name = Config.image_folder+f'/image_{img_counter}.jpg'
        sClient.send_message(cmd)
        sClient.receive_data(file_name)
        print("Picture taken !")
        apps.send_file(file_name)
        img_counter = img_counter+1

    elif(re.search("video",cmd)):
        match = re.search(r'\d+', cmd)
        duration = int(match.group())

        if(duration <= 60):
            file_name = Config.video_folder+f'/video_{vdo_counter}.mp4'
            sClient.send_message(cmd)
            sClient.receive_data(file_name)
            apps.send_file(file_name)
            print(f'Video of {duration} is captured with name : {file_name}')
            vdo_counter = vdo_counter+1
        else:
            print(f'Vidoe duration not valid : {duration}')
            apps.send_msg("Does not support video recording over 60 seconds")

    elif(re.search("image_angle",cmd)):

        file_name = Config.image_folder+f'/image_{img_counter}.jpg'
        match = re.search(r'[+-]?\d+', cmd)
        angle = int(match.group())

        #apps.send_msg(f'Image at angle {angle} taken with name {file_name}')

        if(180 >= angle >= -180):
            sClient.send_message(cmd)
            sClient.receive_data(file_name)
            apps.send_file(file_name)
            img_counter = img_counter+1
        else:
            print(f'Angle value not recognizable : {angle}')
            apps("Invalid Angle Value.")
    
    elif(cmd == "180 record"):

        #apps.send_msg("180 degree video is taken !!!")
        file_name = Config.video_folder+f'/video_{vdo_counter}.mp4'
        sClient.send_message(cmd)
        sClient.receive_data(file_name)
        #cameraControl.record_180video(file_name)
        apps.send_file(file_name)
        vdo_counter = vdo_counter+1
    
    elif(re.search("Exit",cmd)):
        sClient.send_message(cmd)
        apps.send_msg("!!! Session Ended : ALL SAVED FILES WILL BE DELETED !!!")
        # time.sleep(15)
        # osControl.clear_folder(Config.image_folder)
        # time.sleep(5)
        # osControl.clear_folder(Config.video_folder)
        driver.quit()
    
    else:
        apps.send_msg("Invalid Command")

    return img_counter,vdo_counter

def check_continue(cmd):
    if(re.search("continue",cmd)):
        apps.send_msg("Please provide the next command")
        time.sleep(20)
    else:
        sClient.send_message("Exit")
        time.sleep(15)
        apps.send_msg("!!! Session Ended : ALL SAVED FILES WILL BE DELETED !!!")
        # osControl.clear_folder(Config.image_folder)
        time.sleep(5)
        # osControl.clear_folder(Config.video_folder)
        driver.quit()
            



#chrome-driver-setup
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={Config.profile_path}")
options.add_argument(f"profile-directory={Config.profile}")
#options.add_argument("--headless")
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
options.add_argument('--window-size=1920,1080')
options.add_argument("--enable-javascript")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

service = Service(executable_path=Config.exec_path)
driver = webdriver.Chrome(service=service, options=options)

#Can also set this so it will also take the sender dynamically
setup = Wapp_init(Config.def_sender,driver)
apps = Wapp_apps(formatted_user,driver)
img_cnt = 0
vdo_cnt = 0

setup.open_whatsapp()
time.sleep(20)
# driver.save_screenshot("C:/Users/divya/OneDrive/Desktop/test/test2.jpg")
# print("Screenshot taken.")

if(setup.is_element_present(Config.link_mobile)):
    setup.setup_sender()


apps.search_contact()
time.sleep(5)
apps.send_msg(Config.def_msg)
time.sleep(2)
apps.send_msg(Config.instruction)
time.sleep(60)
# cmd = apps.read_msg().pop()
# print("command is : "+cmd)
# time.sleep(10)
# apps.send_msg("Hi, How are you !!")
# time.sleep(15)
# driver.quit()
sClient.connect_to_server(Config.host,Config.port)

while True:
    cmd = apps.read_msg().pop()
    print("command is : "+cmd)
    img_cnt,vdo_cnt = processRequest(apps,cmd,img_cnt,vdo_cnt)
    time.sleep(5)
    apps.send_msg("Please type (continue) to continue the session")
    time.sleep(20)
    nxt_cmd = apps.read_msg().pop()
    check_continue(nxt_cmd)


# text = apps.read_msg()
# print(text.pop())
# apps.send_file("E:/flipped_image_1x.jpg")
# time.sleep(10)
# driver.quit()





