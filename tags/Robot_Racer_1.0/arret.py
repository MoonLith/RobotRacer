"""Lancer ce programme pour reinitialiser tous les ports du Robot"""

import RPi.GPIO as GPIO
import time
import cv2
import Adafruit_PCA9685
import numpy as np

def arret() :
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	pwm = Adafruit_PCA9685.PCA9685()
	pwm.set_pwm_freq(30)

	# ROUES DIRECTIONNELLES
	ROUE = 0  # sortie des roues directionnelles

	# PORT PCA9685
	m1 = 4  # activité du premier moteur
	m2 = 5
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(12, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT)
	pwm.set_pwm(m1, 0, 1200)
	pwm.set_pwm(m2, 0, 1200)
	pwm.set_pwm(ROUE, 0, 230)

	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(12, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)

	GPIO.cleanup()
