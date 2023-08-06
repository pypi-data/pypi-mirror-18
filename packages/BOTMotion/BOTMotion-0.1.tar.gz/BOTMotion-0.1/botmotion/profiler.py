class Position_Profiler():
    def __init__(self, current_pos):
        self.__tick_inc = 50
        self.__max_pos = 4*65536
        self.__min_pos = 0
        self.__current_pos = current_pos

    def next_pos(self):
        if self.__current_pos > self.__max_pos:
            self.__tick_inc = -1*abs(self.__tick_inc)
        elif self.__current_pos < self.__min_pos:
            self.__tick_inc = abs(self.__tick_inc)

        self.__current_pos += self.__tick_inc
        return self.__current_pos

class Velocity_Profiler():
    def __init__(self):
        self.__rpm_inc = 1
        self.__max_velocity = 3000
        self.__min_velocity = 200
        self.__current_velocity = 0

    def next_velocity(self):
        if self.__current_velocity > self.__max_velocity:
            self.__rpm_inc = -1*abs(self.__rpm_inc)
        elif self.__current_velocity < self.__min_velocity:
            self.__rpm_inc = abs(self.__rpm_inc)

        self.__current_velocity += self.__rpm_inc
        return self.__current_velocity
