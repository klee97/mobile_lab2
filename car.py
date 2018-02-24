from mypicar.front_wheels import Front_Wheels
from mypicar.back_wheels import Back_Wheels
from detector_wrapper import DetectorWrapper




def offset(undist, left_fit, right_fit):
	"""
	Calculate vehicle offset from lane center
	"""



def main():
    detector = DetectorWrapper()

    front_wheels = Front_Wheels()
    back_wheels = Back_Wheels()

    try:
        while True:
            success, ret = detector.detect()
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
