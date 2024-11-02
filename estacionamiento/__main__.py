import sys

from estacionamiento.entrada import Entrada
from estacionamiento.ia import (
    EstadiaProcesamientoException,
    PatenteProcesamientoException,
)

# Desactivar __pycache__
sys.dont_write_bytecode = True

entrada = Entrada()

entrada.informar_mensaje("Bienvenido al estacionamiento!")

patente_ok = False
patente: str = ""

while not patente_ok:
    try:
        patente = entrada.obtener_patente()
        patente_ok = True
    except PatenteProcesamientoException:
        entrada.informar_mensaje("No se pudo procesar la patente, intente nuevamente")

reserva = entrada.tiene_reserva(patente)

if reserva:
    entrada.permitir_estacionar(reserva)
else:
    entrada.informar_mensaje("No se encontro reserva")

    estadia_ok = False
    estadia: int = 0

    while not estadia_ok:
        try:
            estadia = entrada.obtener_estadia()
            estadia_ok = True
        except EstadiaProcesamientoException:
            entrada.informar_mensaje(
                "No se pudo procesar la estadia, intente nuevamente"
            )

    reserva = entrada.verificar_espacios(patente, estadia)

    if reserva:
        entrada.permitir_estacionar(reserva)
    else:
        entrada.informar_mensaje(
            "No hay espacio disponible, retire su vehiculo por favor"
        )
