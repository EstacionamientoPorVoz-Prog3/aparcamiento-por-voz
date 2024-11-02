from typing import Optional

from estacionamiento.asistente import Asistente
from estacionamiento.db import BaseDatos, Reserva, Tiempo
from estacionamiento.ia import IA


class Entrada:
    """
    Esta clase maneja la obtencion de la informacion mediante voz
    """

    def __init__(self):
        self.asistente = Asistente()
        self.db = BaseDatos()
        self.ia = IA()

    def obtener_patente(self) -> str:
        mensaje = "¿Podría decirme su patente por favor?"
        print(mensaje)
        self.asistente.habla(mensaje)

        return self.ia.procesar_patente("aca_iria_audio")

    def obtener_estadia(self) -> int:
        mensaje = "¿Cuanto tiempo desea estacionar su vehiculo?"
        print(mensaje)
        self.asistente.habla(mensaje)

        return self.ia.procesar_estadia("aca_iria_audio")

    def verificar_espacios(self, patente: str, estadia: int) -> Optional[Reserva]:
        tiempo = Tiempo()
        tiempo.estadia = estadia
        return self.db.verificar_espacios(patente, tiempo)

    def tiene_reserva(self, patente: str) -> Optional[Reserva]:
        return self.db.tiene_reserva(patente)

    def permitir_estacionar(self, reserva: Reserva):
        self.asistente.habla(f"Estacione en la posición {reserva.posicion}")
        self.db.registrar_vehiculo(reserva)

    def informar_mensaje(self, mensaje: str):
        print(mensaje)
        self.asistente.habla(mensaje)
