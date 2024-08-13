import RPi.GPIO as GPIO
import time

class ServoController:
    # Set up GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    # Define the GPIO pin connected to the servo
    servo_pin = 12

    # Set up the GPIO pin for PWM
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency

    # Function to set servo angle
    def set_angle(self,angle):
        # Map angle from -90~90 to 0~180
        mapped_angle = angle + 90
        duty = mapped_angle / 18 + 2
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)
    
    def rotate_servo_angle(self,angle):
        
        try:
            self.pwm.start(0)
            self.set_angle(angle)
            time.sleep(5)
        finally:
            # Clean up
            self.pwm.stop()
            GPIO.cleanup()

    def rotate_servo(self,cmd):
        
        try:
            self.pwm.start(0)
            if(cmd == "180 degree"):
                # Go to 0 degrees
                print("Moving to 0 degrees")
                self.set_angle(0)
                time.sleep(2)

                # Go to 90 degrees
                print("Moving to 90 degrees")
                self.set_angle(90)
                time.sleep(5)

                # Go to 0 degrees
                print("Moving to 0 degrees")
                self.set_angle(0)
                time.sleep(5)

                # Go to -90 degrees
                print("Moving to -90 degrees")
                self.set_angle(-90)
                time.sleep(5)

                # Go to 0 degrees
                print("Moving to 0 degrees")
                self.set_angle(0)
                time.sleep(2)
                
            elif(cmd == "90 degree right"):
                # Go to 0 degrees
                print("Moving to 0 degrees")
                self.set_angle(0)
                time.sleep(5)

                # Go to 90 degrees
                print("Moving to 90 degrees")
                self.set_angle(90)
                time.sleep(5)

                # Go to 0 degrees
                print("Moving to 0 degrees")
                self.set_angle(0)
                time.sleep(5)

            elif(cmd == "90 degree left"):
                # Go to 0 degrees
                print("Moving to 0 degrees")
                self.set_angle(0)
                time.sleep(5)

                # Go to -90 degrees
                print("Moving to -90 degrees")
                self.set_angle(-90)
                time.sleep(5)

                # Go to 0 degrees
                print("Moving to 0 degrees")
                self.set_angle(0)
                time.sleep(5)

            else:
                print("Servo: unrecognized command")

        finally:
            # Clean up
            self.pwm.stop()
            GPIO.cleanup()

# # Example usage
# if __name__ == "__main__":
#     while True:
#         cmd = input("provide cmd for servo: ")
#         servo_controller = ServoController()
#         servo_controller.rotate_servo(cmd)