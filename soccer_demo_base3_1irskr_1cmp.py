#!/usr/bin/env micropython
import os
import math
import random
from time import sleep
from ev3dev2.motor import Motor, DcMotor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B ,OUTPUT_C ,OUTPUT_D, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor import Sensor
#from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2 import sound
snd=sound.Sound()
rand=random.randint
def dbg(*toPrint):
    if debug:
        print(toPrint)
def ttan(ang):
    return round(math.tan(math.radians(ang)),2)
def tsin(ang):
    return round(math.sin(math.radians(ang)),2)
def tcos(ang):
    return round(math.cos(math.radians(ang)),2)
def tasin(num):
    return round(math.degrees(math.asin(num)),2)
def tatan(num):
    return round(math.degrees(math.atan(num)),2)
def tatan2(a,b):
    return round(math.degrees(math.atan2(a,b)),2)
    
os.system('setfont Lat15-TerminusBold14')
#os.system('setfont Lat15-TerminusBold32x16')
print("start...")

mA=Motor(OUTPUT_A)
mB=Motor(OUTPUT_B)
mC=Motor(OUTPUT_C)
mD=Motor(OUTPUT_D)

def drive(a,b,c,d):
    global mA,mB,mC,mD
    mA.on(SpeedPercent(a))
    mB.on(SpeedPercent(b))
    mC.on(SpeedPercent(c))
    mD.on(SpeedPercent(d))

def motor_cal():
    snd.speak('test motors A.B.C.D')
    drive(100,0,0,0)
    sleep(0.3)
    drive(0,100,0,0)
    sleep(0.3)
    drive(0,0,100,0)
    sleep(0.3)
    drive(0,0,0,100)
    sleep(0.3)
    drive(0,0,0,0)

def compass_cal(compass):
    compass.command='BEGIN-CAL'
    drive(50,50,50,50)
    sleep(2)
    drive(0,0,0,0)
    compass.command='END-CAL'
    sleep(0.5)

def to_heading(h):
    if h > 180:
        return h-360
    else:
        return h

def choose_side(d):
    if d < 5:
        return -1
    else:
        return 1


#motor_cal()
    
skr1 = Sensor(driver_name='ht-nxt-ir-seek-v2', address=INPUT_1)
skr1.mode='AC-ALL'
skr2 = Sensor(driver_name='ht-nxt-ir-seek-v2', address=INPUT_2)
skr2.mode='AC-ALL'
compass = Sensor(driver_name='ht-nxt-compass', address=INPUT_4)
compass.mode='COMPASS'
#compass_cal(compass)
head = to_heading(compass.value(0))

maxP=50 #with rotation 30 pct.
while True:
    dir0 = skr1.value(0)
    dir1 = skr1.value(0)
    dir2 = skr2.value(0)
    if dir1 in range(2,9):
        dir0=dir1
    elif dir2 in range(3,8):
        dir0=dir2+6
    dir0-=1
    
    pwr1 = max([skr1.value(i) for i in range(1,6)])
    pwr2 = max([skr2.value(i) for i in range(1,6)])
    pwr0 = max(pwr1,pwr2)
    
    cmp = to_heading(compass.value(0))
    rot=max(min(cmp-head,30),-30)#this is because value of power cannot go beyond 100%
    print(dir0,pwr0)
    if dir0 not in range(4,7) and pwr1 > 50:
        ang=(choose_side(dir0)*3+dir0-4)*30 #this is for driving towards ball.
    else:
        ang=(dir0-5)*30 #this is for driving towards ball.
    drive(
        tsin(ang)*maxP + rot,
        tcos(ang)*maxP + rot,
        tsin(ang)*maxP*-1 + rot,
        tcos(ang)*maxP*-1 + rot)
    
    