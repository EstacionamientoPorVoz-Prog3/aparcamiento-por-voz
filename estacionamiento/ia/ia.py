import random
from typing import Optional


class ProcesamientoException(Exception):
    pass


class PatenteProcesamientoException(ProcesamientoException):
    pass


class EstadiaProcesamientoException(ProcesamientoException):
    pass


class IA:
    def __init__(self):
        pass

    def procesar_patente(self, audio) -> str:
        # Simula el procesamiento
        # Si falla el procesamiento lanzaria PatenteProcesamientoException
        return "AAA000"

    def procesar_estadia(self, audio) -> int:
        # Simula el procesamiento
        # Si falla el procesamiento lanzaria EstadiaProcesamientoException
        return 5
