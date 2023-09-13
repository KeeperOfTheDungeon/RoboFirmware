from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin('LED'))

pwm.freq(1000)

pwm.duty_u16(32268)

sleep(5)