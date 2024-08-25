from cameraController import CameraController
from servoController import ServoController
from osController import OsController
from socketServer import SocketServer

import config as Config
import time as time
import re
import socket


cameraControl = CameraController()
servoControl = ServoController()
osControl = OsController()
serverControl = SocketServer()

def processRequest(cmd, img_counter, vdo_counter, flag):
    # msg = "Processing Request !!!"
    #serverControl.send_response("Processing Request !!!")
    print("Processing Request !!!")

    if(cmd == "instashot"):
        #serverControl.send_response("Picture taken !")
        print("Picture taken !")
        file_name = Config.image_folder+f'/image_{img_counter}.jpg'
        cameraControl.capture_image(file_name)
        serverControl.send_multimedia(file_name)
        img_counter = img_counter+1

    elif(re.search("video",cmd)):
        match = re.search(r'\d+', cmd)
        duration = int(match.group())

        if(duration <= 60):
            file_name = Config.video_folder+f'/video_{vdo_counter}.mp4'
            cameraControl.record_video(file_name,duration)
            serverControl.send_multimedia(file_name)
            #serverControl.send_response(f'Video of {duration} is captured with name : {file_name}')
            print(f'Video of {duration} is captured with name : {file_name}')
            vdo_counter = vdo_counter+1
        else:
            print(f'Vidoe duration not valid : {duration}')
            serverControl.send_response("Does not support video recording over 60 seconds")

    elif(re.search("image_angle",cmd)):

        file_name = Config.image_folder+f'/image_{img_counter}.jpg'
        match = re.search(r'[+-]?\d+', cmd)
        angle = int(match.group())

        #serverControl.send_response(f'Image at angle {angle} taken with name {file_name}')
        print(f'Image at angle {angle} taken with name {file_name}')

        if(180 >= angle >= -180):
            servoControl.rotate_servo_angle(angle)
            cameraControl.capture_image(file_name)
            serverControl.send_multimedia(file_name)
            img_counter = img_counter+1
            servoControl.rotate_servo_angle(0)
        else:
            print(f'Angle value not recognizable : {angle}')
            serverControl.send_response("Invalid Angle Value.")
    
    elif(cmd == "180 record"):

        #serverControl.send_response("180 degree video is taken !!!")
        file_name = Config.video_folder+f'/video_{vdo_counter}.mp4'
        cameraControl.record_180video(file_name)
        print(f"180 degree video is taken with the name : {file_name}")
        serverControl.send_multimedia(file_name)
        vdo_counter = vdo_counter+1
    
    elif(re.search("Exit",cmd)):
        serverControl.send_response("!!! Session Ended : ALL SAVED FILES WILL BE DELETED !!!")
        time.sleep(15)
        osControl.clear_folder(Config.image_folder)
        time.sleep(5)
        osControl.clear_folder(Config.video_folder)
        flag = True
    
    else:
        serverControl.send_response("Invalid Command")

    return img_counter,vdo_counter,flag

# def check_continue(cmd):
#     if(re.search("continue",cmd)):
#         serverControl.send_response("Please provide the next command")
#         time.sleep(2)
#         serverControl.send_response("For the sake of the loop")
#         time.sleep(20)
#         return False
#     else:
#         serverControl.send_response("!!! Session Ended : ALL SAVED FILES WILL BE DELETED !!!")
#         time.sleep(15)
#         osControl.clear_folder(Config.image_folder)
#         time.sleep(5)
#         osControl.clear_folder(Config.video_folder)
#        return True
            


img_cnt = 0
vdo_cnt = 0
exit_flag = False
serverControl.setup_server(Config.host, Config.port)
#_file.settimeout(60)

try:
    while True:
        if exit_flag:
            break
        else:
            msg = serverControl.handle_messages()
            if msg is None or msg == '':
                print("No valid message received or message is empty. Waiting for the next message...")
                time.sleep(20)
                continue
            img_cnt, vdo_cnt, exit_flag = processRequest(msg, img_cnt, vdo_cnt, exit_flag)
except socket.timeout:
    print("Socket timed out waiting for a message.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    serverControl.close_server()            
      




