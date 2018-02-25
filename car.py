from mypicar.front_wheels import Front_Wheels
from mypicar.back_wheels import Back_Wheels
from detector_wrapper import DetectorWrapper
import numpy as np
import cv2
import math

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
        detector = DetectorWrapper()

        front_wheels = Front_Wheels()
        back_wheels = Back_Wheels()

        try:
                while True:
                        front_wheels.turn_straight()
                        success, ret = detector.detect()
                        frame = ret[0]
                        mid_x = ret[1]
                        left_fit = ret[2]
                        right_fit = ret[3]
                        ploty = ret[4]
                        width,height = frame.shape
                        x2 = endpoint_case1(height/2,left_fit,right_fit)
                        dist = (width/2,0,x2,height/2)
                        adj = x2 - off
                        degree = math.asin(adj/dist)
                        #driving
                        front_wheels.turn(degree)
                        time.sleep(1)
                        detector.plot(ret)
                        if success:
                                print(ret[1])

        except KeyboardInterrupt:
                print("KeboardInterrupt Captured")
        finally:
                detector.stop()
                back_wheels.stop()
                front_wheels.turn_straight()


if __name__ == '__main__':
        main()
