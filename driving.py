from mypicar.front_wheels import Front_Wheels
from mypicar.back_wheels import Back_Wheels
from detector_wrapper import DetectorWrapper
import numpy as np
import cv2
import math
import time
import argparse

'''
Main function to run self-driving program.
Supports commandline arguments for threshold, turning angle, and frame off set
'''
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--frame',help = 'Specifies frameOffSet (car location based on frame)')
    parser.add_argument('-t','--thresh',help = 'Specifies a particular threshold to test. i.e. 20')
    parser.add_argument('-d','--degree',help = 'Specifies a particular angle to turn')
    args = parser.parse_args()

    #car location based on frame. Default is 300, optimal value for driving in lab3
    if args.frame:
        frameOff = float(args.frame)
    else:
        frameOff = 300
       
    #allowed car distance from the middle of lane. Default is 20, optimal value for driving in lab3
    if args.thresh:
        thresh = float(args.thresh)
    else:
        thresh = 20

    #turning degree. Default is 15, optimal value for driving in lab3
    if args.degree:
        degree = float(args.degree)       
    else:
        degree = 15       

    #initialize car
    detector = DetectorWrapper()
    front_wheels = Front_Wheels()
    back_wheels = Back_Wheels()

    #Main program for self-driving. Each action of straight driving or turned driving
    #all last time.sleep(1)
    try:
        while True:
            front_wheels.turn_straight()
            success, ret = detector.detect()

            #skips if lane not detected in current frame
            if not success:
                continue

            #displays camera capturing of lane detection
            detector.plot(ret)

            mid_x = ret[1]

            #distance to lane center.
            distance = mid_x - frameOff

            #driving speed is set to 25
            back_wheels.speed = 25

            #If distance to lane center is positive, then turn right
            # If distance is negative, then turn left
            if distance > thresh:
                front_wheels.turn_rel(degree)
            elif distance < -thresh:
                front_wheels.turn_rel(-degree)
            else:
                front_wheels.turn_straight()

            back_wheels.forward()
            time.sleep(1)

    except KeyboardInterrupt:
        print("KeboardInterrupt Captured")
    #clean up
    finally:
        detector.stop()
        back_wheels.stop()
        front_wheels.turn_straight()


if __name__ == '__main__':
    main()
