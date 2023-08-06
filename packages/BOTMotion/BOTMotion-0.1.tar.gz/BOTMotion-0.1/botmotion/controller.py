#!/usr/bin/env python

import spnav
import pygame
import math


from bot_motion import *

DEBUG = True

VELOCITY_FACTOR = 200
ANGLE_FACTOR = 5

LOW_SPEED_THRESHOLD = 10

MAX_SPEED = 2000
WHEEL_RADIUS = 0.0525  # //in meters
LENGTH_BETWEEN_FRONT_REAR_WHEELS = 0.23  # //in meters
LEGNTH_BETWEEN_FRONT_WHEELS = 0.25  # //in meters
L1 = LEGNTH_BETWEEN_FRONT_WHEELS / 2.0
L2 = LENGTH_BETWEEN_FRONT_REAR_WHEELS / 2.0


class VelocityCalcul(threading.Thread):
    """DOCSTRIN
    g for ClassName"""

    def __init__(self, q_in, q_out_motor):
        super(VelocityCalcul, self).__init__()
        self.q_in = q_in
        self.q_out_motor = q_out_motor
        self.desired_velocity = []
        self.__alive = threading.Event()
        self.__alive.set()


    def e_function(self, val):
        #print val
        ret = math.pow((math.e * (MAX_SPEED / math.e)), math.fabs(val))
        if val > 0:
            return ret
        else:
            return ret * -1

    def high_speed_filter(self, val):
        if (val > MAX_SPEED):
            return MAX_SPEED
        elif (val < -MAX_SPEED):
            return -MAX_SPEED
        else:
            return val


    def close(self):
        #self.q_out_motor.join()
        #self.q_in.join()
        self.__alive.clear()
        #self.join()

    def run(self):
        while self.__alive.isSet():
            if not self.q_in.empty():
                self.desired_velocity = []
                val = self.q_in.get()
                linear_x = val[1]
                linear_y = val[0]*-1
                angular_z = val[2]*-ANGLE_FACTOR
                #print 'X: %f, Y: %f, angle: %f' % (linear_x, linear_y, angular_z)

                # axis0 = ( (-1.0 * (-linear_x + linear_y -  angular_z)) * VELOCITY_FACTOR)
                # axis1 = ( (-1.0 * (-linear_x - linear_y +  (-1.0) * angular_z)) * VELOCITY_FACTOR)
                # axis2 = ( ((-linear_x - linear_y - (-1.0) * angular_z)) * VELOCITY_FACTOR)
                # axis3 = ( ((-linear_x + linear_y + angular_z)) * VELOCITY_FACTOR)
                #
                # axis0 = self.e_function(axis0)
                # axis1 = self.e_function(axis1)
                # axis2 = self.e_function(axis2)
                # axis3 = self.e_function(axis3)
                #
                # # High speed filter
                # axis0 = self.high_speed_filter(axis0)
                # axis1 = self.high_speed_filter(axis1)
                # axis2 = self.high_speed_filter(axis2)
                # axis3 = self.high_speed_filter(axis3)

                axis0 = int( (-1.0 * (-linear_x + linear_y - (L1 + L2) * angular_z) / WHEEL_RADIUS) * VELOCITY_FACTOR)
                axis1 = int( (-1.0 * (-linear_x - linear_y + (L1 + L2) * (-1.0) * angular_z) / WHEEL_RADIUS) * VELOCITY_FACTOR)
                axis2 = int( ((-linear_x - linear_y - (L1 + L2) * (-1.0) * angular_z) / WHEEL_RADIUS) * VELOCITY_FACTOR)
                axis3 = int( ((-linear_x + linear_y + (L1 + L2) * angular_z) / WHEEL_RADIUS) * VELOCITY_FACTOR)

                # Low speed filter
                axis0 = 0 if abs(axis0) < LOW_SPEED_THRESHOLD else axis0
                axis1 = 0 if abs(axis1) < LOW_SPEED_THRESHOLD else axis1
                axis2 = 0 if abs(axis2) < LOW_SPEED_THRESHOLD else axis2
                axis3 = 0 if abs(axis3) < LOW_SPEED_THRESHOLD else axis3

                self.desired_velocity.append(axis0)
                self.desired_velocity.append(axis1)
                self.desired_velocity.append(axis2)
                self.desired_velocity.append(axis3)
                #print "desired velocity = (%f, %f, %f, %f)" % (self.desired_velocity[0], self.desired_velocity[1], self.desired_velocity[2], self.desired_velocity[3])
                self.q_out_motor.put(self.desired_velocity)
                self.q_in.task_done()

        print '[VelCalc] Exit Thread...'

class JoystickPosition(threading.Thread):
    def __init__(self, q):
        super(JoystickPosition, self).__init__()
        self.q = q
        self.posit = []
        self.__alive = threading.Event()
        self.__alive.set()

    def close(self):
        print 'Shutdown Joystick'
        self.__alive.clear()
        #self.join()
        pygame.quit()

    def run(self):
        pygame.init()
        # Grab joystick 0
        if pygame.joystick.get_count() == 0:
            raise IOError("No joystick detected")
        joy = pygame.joystick.Joystick(0)
        joy.init()
        axes = [0.0] * joy.get_numaxes()

        while self.__alive.isSet():
            # Pump and che1ck the events queue
            pygame.event.pump()

            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif events.type == pygame.JOYAXISMOTION:
                    self.posit = []
                    e = events.dict
                    axes[e['axis']] = e['value']
                    # print "axes [0] = ", e['value']
                    self.posit.append(axes[0])
                    self.posit.append(axes[1])
                    self.posit.append(axes[2])
                    #print "Joystick Position (%0.2f, %0.2f, %0.2f)" % (self.posit[0], self.posit[1], self.posit[2])
                    self.q.put(self.posit)


class SpaceNavPosition(threading.Thread):
    def __init__(self, q):
        super(SpaceNavPosition, self).__init__()
        self.q = q
        self.trans = []
        self.__alive = threading.Event()
        self.__alive.set()
        try:
            spnav.spnav_open()
        except spnav.SpnavConnectionException as e:
            raise e


    def close(self):
        self.__alive.clear()
        #print '[SpNav] Shutdown'
        threading.Thread.join(self, None)
        spnav.spnav_close()

    def run(self):
        while self.__alive.isSet():
            event = spnav.spnav_poll_event()

            if event and event.ev_type == spnav.SPNAV_EVENT_MOTION:
                self.trans = []
                self.trans.append(event.translation[2]/350.0)
                self.trans.append(event.translation[0]/350.0)
                self.trans.append(event.rotation[1]/350.0)
                self.q.put(self.trans)
            else:
                self.trans = []
                self.trans.append(0.0)
                self.trans.append(0.0)
                self.trans.append(0.0)
                self.q.put(self.trans)

            spnav.spnav_remove_events(spnav.SPNAV_EVENT_ANY)
            spnav.spnav_remove_events(spnav.SPNAV_EVENT_MOTION)
            spnav.spnav_remove_events(spnav.SPNAV_EVENT_BUTTON)
            time.sleep(0.05)

        print '[SpNav] Exit Thread...'

# main
def main():
    q_input_dev = Queue.Queue()
    q_motor = Queue.Queue()


    spnavThread = None
    velocityCalculator = None
    joystickThread = None
    motor_list = []
    printer = None

    try:
        while False:
            input_device = raw_input("Please choose the device to control the robot: 1) Space Navigator 2) Joystick [1/2]? : ")
            # check if d1a is equal to one of the strings, specified in the list
            if input_device in ['1', '2']:
                # if it was equal - break from the while loop
                break

        input_device = '1'

        # process the input
        if input_device == "1":
            print ("Move the Space Navigator to control the robot..")

            spnavThread = SpaceNavPosition(q_input_dev)
            spnavThread.start()

        elif input_device == "2":
            print ("Move the Joystick to control the robot..")
            # main loop
            joystickThread = JoystickPosition(q_input_dev)
            joystickThread.start()
            # main loop

        velocityCalculator = VelocityCalcul(q_input_dev, q_motor)
        velocityCalculator.start()
        q_input_dev.join()


        #motor_list.append(BotMotion('192.168.101.221'))
        #motor_list.append(BotMotion('192.168.101.222'))
        #motor_list.append(BotMotion('192.168.101.223'))
        motor_list.append(BotMotion('192.168.101.224', 'CSV'))
        printer = Printing()
        #printer.init()
        l_velo = {0,0,0,0}
        while True:
            if not q_motor.empty():
                l_velo = q_motor.get()
                q_motor.task_done()

                motor_list[0].set_velocity(l_velo[0])
                #motor_list[1].set_velocity(l_velo[1])
                #motor_list[2].set_velocity(l_velo[2])
                #motor_list[3].set_velocity(l_velo[3])

            pdo_in = motor_list[0].get_pdo_in()
            pdo_out = motor_list[0].get_pdo_out()

            #printer.print_pdo(pdo_in, pdo_out)



                    # if counter==30:
                    #     print "[%s] (%5d, %5d, %5d, %5d)" % (time.strftime('%S'), l_velo[0], l_velo[1], l_velo[2], l_velo[3])
                    #     counter = 0
                    # counter += 1
    except Exception as e:
        print 'Exception:', e
        print 'Exit...'
    except KeyboardInterrupt:
        print 'Exit...'
    finally:
        if printer:
            printer.close()
        for motor in motor_list:
            motor.close()

        if velocityCalculator:
            velocityCalculator.close()

        if spnavThread:
            spnavThread.close()

    sys.exit(0)

        # if joystickThread:
        #     joystickThread.close()


if __name__ == '__main__':
    main()




