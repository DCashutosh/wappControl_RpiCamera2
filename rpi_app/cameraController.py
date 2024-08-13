from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

from servoController import ServoController
import time
import logging

class CameraController:
    logging.basicConfig(level=logging.DEBUG)
    picam2 = Picamera2()
    servoControl = ServoController()

    def capture_image(self,file_name):
        try:
            full_resolution = self.picam2.sensor_resolution

            # Apply both horizontal and vertical flip
            transform = Transform(hflip=1, vflip=1)

            config = self.picam2.create_still_configuration(
                main={"size": full_resolution},
                lores={"size": (640, 480)},
                transform=transform,
                display="lores"
            )
            self.picam2.configure(config)

            self.picam2.start()
            time.sleep(2)  # Wait for camera to initialize

            self.picam2.capture_file(file_name) #file_name can be an address
            print(f"Image captured successfully: {file_name}")

        except Exception as e:
            print(f"Error capturing image: {str(e)}")
            logging.exception("Detailed error information:")
        
        finally:
             if self.picam2:
                  self.picam2.stop()
        
    
    def record_video(self,file_name,duration):
        transform = Transform(hflip=1, vflip=1)

        video_config = self.picam2.create_video_configuration(
            main={"size": (1920, 1080)},
            transform=transform
        )
        self.picam2.configure(video_config)
        #self.picam2.start()
        #time.sleep(2)

        encoder = H264Encoder(bitrate=10000000)
        output = FfmpegOutput(file_name) #need to modify so that the video will be saved on a specific folder

        self.picam2.start_recording(encoder, output)

        print(f"Recording video for {duration} seconds.")
        time.sleep(duration)

        self.picam2.stop_recording()
        self.picam2.stop()

        print("Video recording completed.")
    
    def record_180video(self,file_name):
        transform = Transform(hflip=1, vflip=1)

        video_config = self.picam2.create_video_configuration(
            main={"size": (1920, 1080)},
            transform=transform
        )
        self.picam2.configure(video_config)
        #self.picam2.start()
        #time.sleep(2)

        encoder = H264Encoder(bitrate=10000000)
        output = FfmpegOutput(file_name) #need to modify so that the video will be saved on a specific folder

        self.picam2.start_recording(encoder, output)

        print(f"Recording 180 degree video")
        self.servoControl.rotate_servo("180 degree")

        self.picam2.stop_recording()
        self.picam2.stop()

        print("180 degree Video recording completed.")
    
    def close_camera(self):
        if self.picam2:
                self.picam2.stop()
                self.picam2.close()


# # Example usage
# if __name__ == "__main__":
#     camera_controller = CameraController()
#     camera_controller.record_video("test_video.mp4",60)