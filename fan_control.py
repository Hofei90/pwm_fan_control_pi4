import datetime
import os
import time

import gpiozero
import toml
from gpiozero.pins.pigpio import PiGPIOFactory

STEP_WIDTH = 5
ON_OFF_HYSTERESIS = 5
SKRIPTPFAD = os.path.abspath(os.path.dirname(__file__))
factory = PiGPIOFactory()
PWM_FAN = gpiozero.PWMOutputDevice(18, pin_factory=factory)
TACHO_PIN = gpiozero.Button(23)


def load_config(pfad=SKRIPTPFAD):
    configfile = os.path.join(pfad, "config.toml")
    with open(configfile) as conffile:
        config = toml.loads(conffile.read())
    return config


CONFIG = load_config()


class Tacho:
    def __init__(self):
        self.start_time = None
        self.current_measurement = 0
        self.last_measurement = datetime.datetime.now()

    def frequence_counter_start(self):
        TACHO_PIN.when_pressed = self.counter_increment
        self.start_time = datetime.datetime.now()

    def frequence_counter_stop(self):
        TACHO_PIN.when_pressed = None
        self.process_results()

    def counter_increment(self):
        now = datetime.datetime.now()
        self.current_measurement = (now - self.last_measurement).total_seconds()
        self.last_measurement = now

    def process_results(self):
        try:
            current_measurement = 1 / self.current_measurement
        except ZeroDivisionError:
            current_measurement = 0
        print(f"Measurement: {current_measurement}")
        print(current_measurement / 2 * 60)


def round_temperature(x, base=STEP_WIDTH):
    return base * round(x / base)


def generate_all_temperatures_dutycycles(temperatures_dutycycles):
    last_data = 0
    all_temperatures_dutycycles = {}
    for temperature in range(0, 100 + STEP_WIDTH, STEP_WIDTH):
        if temperature in temperatures_dutycycles:
            all_temperatures_dutycycles[temperature] = temperatures_dutycycles[temperature]
            last_data = temperatures_dutycycles[temperature]
        else:
            all_temperatures_dutycycles[temperature] = last_data
    return all_temperatures_dutycycles


def read_temperature():
    return gpiozero.CPUTemperature().value * 100


def set_pwm_speed(dutycycle):
    PWM_FAN.value = dutycycle / 100


def main():
    PWM_FAN.on()
    temperatures_dutycycles = {data[0]: data[1] for data in CONFIG["pwm"]}
    temperatures_dutycycles = generate_all_temperatures_dutycycles(temperatures_dutycycles)
    while True:
        tacho = Tacho()
        tacho.frequence_counter_start()
        while (datetime.datetime.now() - tacho.start_time).total_seconds() < 1:
            time.sleep(0.02)
        tacho.frequence_counter_stop()
        temperature = read_temperature()
        temperature_rounded = round_temperature(temperature)
        new_dutycycle = temperatures_dutycycles[temperature_rounded]
        if new_dutycycle != PWM_FAN.value * 100:
            if new_dutycycle == 0:
                temperature_rounded = round_temperature(temperature_rounded + ON_OFF_HYSTERESIS)
            set_pwm_speed(temperatures_dutycycles[temperature_rounded])
        # TODO: Logging einbauen
        # print(f"Temperatur: {temperature}, {temperature_rounded}, DutyCycle: {PWM_FAN.value * 100}%")
        time.sleep(3)


if __name__ == "__main__":
    main()
