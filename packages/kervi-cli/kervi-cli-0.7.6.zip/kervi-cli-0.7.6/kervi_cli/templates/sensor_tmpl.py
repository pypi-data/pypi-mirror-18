""" Module for a sensor """
from kervi.sensor import Sensor, SensorThread

class MySensor(Sensor):
    """ My sensor """
    def __init__(self):
        Sensor.__init__(self, "mySensor", "My sensor")
        self.type = "temp"
        self.max = 100
        self.min = 0
        self.reading_interval = 10
        self.unit = "C"
        self.dashboards = ["main"]

        #variables needed for my sensor
        self.counter = 0 #dummy counter
        self.counter_delta = 1

    def read_sensor(self):
        #read_sensor is called with self.reading_interval
        #snippet below is just dummy code
        #enter your real code here to read your sensor

        self.counter += self.counter_delta

        if self.counter > self.max:
            self.counter_delta = -1
        elif self.counter <= self.min:
            self.counter_delta = 1

        #call new_sensor_reading to signal a new value
        self.new_sensor_reading(self.counter)

MY_SENSOR_THREAD = SensorThread(MySensor())
