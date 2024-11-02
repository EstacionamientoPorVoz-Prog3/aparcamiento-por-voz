import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class Tiempo:
    dia: int = 30
    mes: int = 10
    anio: int = 2024
    hora: int = 10
    minutos: int = 30
    estadia: int = 5


@dataclass
class Reserva:
    patente: str
    tiempo: Tiempo
    posicion: int


class BaseDatos:
    """
    Esta clase es una abstracción del accesso a la base de datos
    """

    def __init__(self):
        pass

    def tiene_reserva(self, patente: str) -> Optional[Reserva]:
        # Simula la consulta
        random.choice(
            [
                Reserva(patente, Tiempo(), 5),
                None,
            ]
        )

    def verificar_espacios(self, patente: str, tiempo: Tiempo) -> Optional[Reserva]:
        # Simula la consulta, si hay espacio le asigna uno y retorna la reserva
        # Si no no retorna nada
        return random.choice([Reserva(patente, tiempo, 5), None])

    def registrar_vehiculo(self, reserva: Reserva):
        # Simula el registro
        print(
            f"Vehiculo con {reserva.patente} registrado en la {reserva.posicion} durante {reserva.tiempo.estadia} hs."
        )
