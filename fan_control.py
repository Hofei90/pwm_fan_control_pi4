import datetime
import os
import time

import gpiozero
import toml
from gpiozero.pins.pigpio import PiGPIOFactory

SCHRITTWEITE = 5
ON_OFF_HYSTERESE = 5
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
        self.startzeit = None
        self.messung = 0
        self.messung_old = datetime.datetime.now()

    def start_frequenzzaehlung(self):
        TACHO_PIN.when_pressed = self.zaehler_erhoehen
        self.startzeit = datetime.datetime.now()

    def stop_frequenzzaehlung(self):
        TACHO_PIN.when_pressed = None
        self.ergebnisse_auswerten()

    def zaehler_erhoehen(self):
        now = datetime.datetime.now()
        self.messung = (now - self.messung_old).total_seconds()
        self.messung_old = now

    def ergebnisse_auswerten(self):
        try:
            messung = 1 / self.messung
        except ZeroDivisionError:
            messung = 0
        print(f"Messung: {messung}")
        print(messung / 2 * 60)


def myround(x, base=SCHRITTWEITE):
    return base * round(x / base)


def generate_all_temperatures_dutycycles(temperatures_dutycycles):
    last_data = 0
    all_temperatures_dutycycles = {}
    for temperatur in range(0, 100 + SCHRITTWEITE, SCHRITTWEITE):
        if temperatur in temperatures_dutycycles:
            all_temperatures_dutycycles[temperatur] = temperatures_dutycycles[temperatur]
            last_data = temperatures_dutycycles[temperatur]
        else:
            all_temperatures_dutycycles[temperatur] = last_data
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
        tacho.start_frequenzzaehlung()
        while (datetime.datetime.now() - tacho.startzeit).total_seconds() < 1:
            time.sleep(0.02)
        tacho.stop_frequenzzaehlung()
        temperatur = read_temperature()
        round_temperatur = myround(temperatur)
        new_dutycycle = temperatures_dutycycles[round_temperatur]
        if new_dutycycle != PWM_FAN.value * 100:
            if new_dutycycle == 0:
                round_temperatur = myround(round_temperatur + ON_OFF_HYSTERESE)
            set_pwm_speed(temperatures_dutycycles[round_temperatur])
        print(f"Temperatur: {temperatur}, {round_temperatur}, DutyCycle: {PWM_FAN.value * 100}%")
        time.sleep(3)


if __name__ == "__main__":
    main()
