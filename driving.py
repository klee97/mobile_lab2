from mypicar.front_wheels import Front_Wheels
from mypicar.back_wheels import Back_Wheels
from detector_wrapper import DetectorWrapper
import numpy as np
import cv2
import math
import time
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--frame',help = 'Specifies frameOffSet (car location based on frame)')
    parser.add_argument('-t','--thresh',help = 'Specifies a particular threshold to test. i.e. 20')
    parser.add_argument('-d','--degree',help = 'Specifies a particular angle to turn')
    args = parser.parse_args()

    #car location based on frame
    if args.frame:
        frameOff = float(args.frame)
    else:
        frameOff = 300
        

    if args.thresh:
        thresh = float(args.thresh)
    else:
        thresh = 20

    if args.degree:
        degree = float(args.degree)
        
    else:
        degree = 15
        
    
    detector = DetectorWrapper()

    front_wheels = Front_Wheels()
    back_wheels = Back_Wheels()
    left = 0
    try:
        while True:
            front_wheels.turn_straight()
            success, ret = detector.detect()
            if not success:
                continue

            detector.plot(ret)
            
            frame = ret[0]
            mid_x = ret[1]
            left_fit = ret[2]
            right_fit = ret[3]
            ploty = ret[4]        
            width = frame.shape[0]
            height = frame.shape[1]

            #distance to lane center. If distance if positive, then turn right
            # If distance is negative, then turn left
            distance = mid_x - frameOff
            
            back_wheels.speed = 25
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
    finally:
        detector.stop()
        back_wheels.stop()
        front_wheels.turn_straight()


if __name__ == '__main__':
    main()
