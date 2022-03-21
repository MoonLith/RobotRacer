
import RPi.GPIO as GPIO
import Adafruit_PCA9685

camera = cv2.VideoCapture(0)
ret = camera.set(3,192);
ret = camera.set(4,108);

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(30)
MOTOR_A1 = 11
MOTOR_A2 = 12
# MOTEUR DROITE
MOTOR_B1 = 18
MOTOR_B2 = 16

ROUE = 0  # sortie des roues directionnelles

# PORT PCA9685
m1 = 4  # activité du premier moteur
m2 = 5
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
pwm.set_pwm(m1, 0, 1200)
pwm.set_pwm(m2, 0, 1200)

GPIO.output(11, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(12, GPIO.LOW)
GPIO.output(16, GPIO.LOW)

GPIO.cleanup()
