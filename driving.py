from mypicar.front_wheels import Front_Wheels
from mypicar.back_wheels import Back_Wheels
from detector_wrapper import DetectorWrapper
import numpy as np
import cv2
import math
import time
import argparse

def offset(frame,mid_x):
    """
    Calculate vehicle offset from lane center
    """
        
    frame = cv.flip(frame,0)
    out.write(frame)
    img = cv.imread('frame',frame)
    height, width, channels = img.shape
    off = mid_x - width
    return off

def widthH(frame):
    """
    Calculate frame width and height
    """        
    frame = cv.flip(frame,0)
    out.write(frame)
    img = cv.imread('frame',frame)
    height, width, channels = img.shape
    return (width,height)	

def endpoint_case1(height, left_fit, right_fit):
    '''
    both parabolas intersect height of frame
    '''
    print left_fit[0], left_fit[1], left_fit[2]
    x1 = left_fit[0] * height**2 + left_fit[1] * height + left_fit[2]
    x2 = right_fit[0] * height**2 + right_fit[1] * height + right_fit[2]
    return x2 - x1


def dist(x1, y1, x2, y2):
    '''
    Distance function for cartesian coordinates
    Inputs: - transmitter coordinates (tx, ty) 
            - receiver coordinates (rx, ry)
    Output: Distance between the two points 
    '''
    d = math.pow(x2 - x1, 2) + math.pow(y2-y1, 2)
    return math.sqrt(d)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--frame',help = 'Specifies frameOffSet (car location based on frame)')
    parser.add_argument('-t','--thresh',help = 'Specifies a particular threshold to test. i.e. 20')
    parser.add_argument('-d','--degree',help = 'Specifies a particular angle to turn')
    args = parser.parse_args()

    #car location based on frame
    if args.frame:
        frameOff = args.frame
    else:
        frameOff = 233

    if args.thresh:
        thresh = args.thresh
    else:
        thresh = 20

    if args.degree:
        degree = args.degree
    else:
        degree = 10
        
    
    detector = DetectorWrapper()

    front_wheels = Front_Wheels()
    back_wheels = Back_Wheels()
    left = 0
    try:
        while True:
            front_wheels.turn_straight()
 #           time.sleep(1)
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
            print "width", width
            height = frame.shape[1]
            print "height", height
            print "mid_x", mid_x

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
