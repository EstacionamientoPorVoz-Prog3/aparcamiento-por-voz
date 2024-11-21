import math
import random
import re
import wave
from typing import Optional

import pyaudio
import whisper


class ProcesamientoException(Exception):
    pass


class PatenteProcesamientoException(ProcesamientoException):
    pass


class EstadiaProcesamientoException(ProcesamientoException):
    pass


class ConfirmacionProcesamientoException(ProcesamientoException):
    pass


class IA:
    FORMATO = pyaudio.paInt16
    CANALES = 1
    RATE = 44100
    CHUNK = 512
    SEGUNDOS_GRABACION = 7
    NOMBRE_ARCHIVO = "audiotemp.wav"
    AFIRMATIVO = [
        "bueno",
        "joya",
        "dale",
        "de una",
        "si",
        "sí",
        "perfecto",
        "buenisimo",
        "buenisímo",
    ]
    NEGATIVO = [
        "no",
        "nah",
        "neh",
        "ni ahi",
        "ni ahí",
        "ni loco",
    ]

    def __init__(self, audio: pyaudio.PyAudio, id_dispositivo: int):
        self.audio = audio
        self.modelo = whisper.load_model("turbo", device="cpu")
        self.id_dispositivo = id_dispositivo
        pass

    def recibir_audio_a_str(self) -> str:
        stream = self.audio.open(
            format=self.FORMATO,
            channels=self.CANALES,
            rate=self.RATE,
            input=True,
            input_device_index=self.id_dispositivo,
            frames_per_buffer=self.CHUNK,
        )

        frames_grabados = []

        for _a in range(0, math.ceil(self.RATE / self.CHUNK * self.SEGUNDOS_GRABACION)):
            data = stream.read(self.CHUNK)
            frames_grabados.append(data)

        stream.stop_stream()
        stream.close()

        archivo = wave.open(self.NOMBRE_ARCHIVO, "wb")
        archivo.setnchannels(self.CANALES)
        archivo.setsampwidth(self.audio.get_sample_size(self.FORMATO))
        archivo.setframerate(self.RATE)
        archivo.writeframes(b"".join(frames_grabados))
        archivo.close()

        resultado = self.modelo.transcribe(self.NOMBRE_ARCHIVO, language="es")

        return resultado["text"].__str__()

    def procesar_patente(self) -> str:
        texto_desde_audio = self.recibir_audio_a_str()

        valido, patente = self.extraer_patente(texto_desde_audio)

        if not valido:
            raise PatenteProcesamientoException()

        return patente

    def extraer_tiempo(self, texto: str):
        texto = texto.lower()
        texto = texto.replace("una", "1")
        texto = texto.replace("media", "30")
        texto = texto.replace("cuarto", "15")
        palabras = texto.strip().split()

        numeros = []
        for palabra in palabras:
            if palabra[0].isdigit():
                numeros.append(int(palabra))
            if len(numeros) < 1:
                numeros.append(0)
            if len(numeros) < 2:
                numeros.append(0)
        return (numeros[0], numeros[1])

    def procesar_estadia(self) -> int:
        texto_desde_audio = self.recibir_audio_a_str()

        horas, minutos = self.extraer_tiempo(texto_desde_audio)

        minutos_total = (horas * 60) + minutos

        if minutos_total <= 0:
            raise EstadiaProcesamientoException()

        return minutos_total

    def procesar_confirmacion(self) -> bool:
        texto_desde_audio = self.recibir_audio_a_str()

        confirmacion = self.extraer_confirmacion(texto_desde_audio)

        if confirmacion is None:
            raise ConfirmacionProcesamientoException()

        return confirmacion

    def extraer_confirmacion(self, texto: str) -> Optional[bool]:
        texto = texto.lower()
        if texto in self.AFIRMATIVO:
            return True
        elif texto in self.NEGATIVO:
            return False
        else:
            return None

    def extraer_patente(self, texto: str):
        texto_limpio = "".join(c for c in texto if c.isalnum())

        patrones = {
            "actual": r"[A-Z]{2}\d{3}[A-Z]{2}",  # AA123BB
            "anterior": r"[A-Z]{3}\d{3}",  # ABC123
            "moto": r"[A-Z]\d{3}[A-Z]{3}",  # A123BCD
        }

        for _tipo, patron in patrones.items():
            match = re.search(patron, texto_limpio)
            if match:
                return (True, texto_limpio)

        return (False, texto_limpio)
