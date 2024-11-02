import random

import pyttsx3

from estacionamiento.db import BaseDatos


class Asistente:
    def __init__(self, velocidad: int = 150, volumen: float = 1.0):

        self.motor = pyttsx3.init()

        self.motor.setProperty("rate", velocidad)
        self.motor.setProperty("volume", volumen)

        self.voces = self.motor.getProperty("voices")

    def habla(self, mensaje: str):
        self.motor.say(mensaje)
        self.motor.runAndWait()
