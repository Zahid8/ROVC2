#import RPi.GPIO
#import RPi.GPIO
import pigpio
import numpy as np
from pysticks import get_controller
con = get_controller()

thruster_1 = 9    #Enter the PIN Number to Which Thrsuter 1 is coonected
thruster_2 = 11    #Enter the PIN Number to Which Thrsuter 2 is coonected
thruster_3 = 25  #Enter the PIN Number to Which Thrsuter 3 is coonected
thruster_4 = 8
thruster_pins = [thruster_1,thruster_2,thruster_3,thruster_4]
thvalue = [1500,1500,1500,1500] 
pi = pigpio.pi()
for item in thruster_pins:
    pi.set_servo_pulsewidth(item,1500)



def map_values(value):
    if value < -1 or value > 1:
        return None
    elif value == 0:
        return 1500
    else:
        return int(1500 + (value * 300))    

def sig(value):
    if value < -1 or value > 1:
        return None
    elif value == 0:
        return 1500
    else:
        return int((np.sign(value) * (27*(abs(value)) - 1) / (27*(1) - 1)) * 300 + 1500)   

def nullify(value):
    return 1500

def forward():
    con.update()

    # move=map_values(con.getPitch())
    # turn=map_values(con.getRoll())
    move=map_values(con.getPitch())
    turn=sig(con.getYaw())

    if turn == 1500 and move == 1500:
        pi.set_servo_pulsewidth(thruster_1, 1500)
        pi.set_servo_pulsewidth(thruster_3, 1500)
        print(move)
    elif turn!=1500: 
        pi.set_servo_pulsewidth(thruster_1, turn+50)
        pi.set_servo_pulsewidth(thruster_3, turn-50)
        print("Thruster 1: ", turn+50)
        print("Thruster 2: ", turn-50)
    elif move!=1500: 
        pi.set_servo_pulsewidth(thruster_1, move)
        pi.set_servo_pulsewidth(thruster_3, move)
        print("forward thrust: ", move)


while(1):
    forward()