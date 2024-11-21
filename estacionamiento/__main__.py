import sys

import pyaudio

from estacionamiento.entrada import Entrada
from estacionamiento.ia import (
    EstadiaProcesamientoException,
    PatenteProcesamientoException,
)

# Desactivar __pycache__
sys.dont_write_bytecode = True

device_index = 2
audio = pyaudio.PyAudio()

print("----------------------Lista de dispositivos de entrada---------------------")
info = audio.get_host_api_info_by_index(0)
info_cantidad = info.get("deviceCount")
numero_dispositivos = int(info_cantidad) if info_cantidad is not None else 0

for i in range(0, numero_dispositivos):
    canales = audio.get_device_info_by_host_api_device_index(0, i).get(
        "maxInputChannels", 0
    )
    if int(canales) > 0:
        print(
            f'Id dispositivo {i} - {audio.get_device_info_by_host_api_device_index(0, i).get("name")}'
        )

print("-------------------------------------------------------------")

idx = int(input())
print(f"Se tomara el audio con el dispositivo {idx}")

entrada = Entrada(audio, idx)
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
