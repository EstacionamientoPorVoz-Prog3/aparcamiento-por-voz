import sys

import pyaudio

from estacionamiento.entrada import Entrada
from estacionamiento.ia import (
    EstadiaProcesamientoException,
    PatenteProcesamientoException,
)
from estacionamiento.ia.ia import ConfirmacionProcesamientoException

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
            f'Id dispositivo {
                i} - {audio.get_device_info_by_host_api_device_index(0, i).get("name")}'
        )

print("---------------------------------------------------------------------------")

idx = int(input().strip())
print(f"Se tomara el audio con el dispositivo {idx}")
entrada = Entrada(audio, idx)

while True:
    input("Esperando llegada de un auto")

    entrada.informar_mensaje("Bienvenido al estacionamiento!")

    patente_ok = False
    confirmacion = False
    patente: str = ""

    while not patente_ok:
        try:
            patente = entrada.obtener_patente()
            patente_ok = True
            confirmacion = False
            while not confirmacion:
                try:
                    mensaje = f"Entendí {patente} ¿Es esto correcto?"
                    confirmacion = entrada.obtener_confirmacion(mensaje)
                    if not confirmacion:
                        entrada.informar_mensaje(
                            "Vuelva a indicar su patente por favor")
                        patente_ok = False
                        confirmacion = True
                    else:
                        entrada.informar_mensaje(
                            f"Patente {patente} confirmada!")
                except ConfirmacionProcesamientoException:
                    entrada.informar_mensaje(
                        "No se pudo procesar la confirmacion, intente nuevamente"
                    )

        except PatenteProcesamientoException:
            entrada.informar_mensaje(
                "No se pudo procesar la patente, intente nuevamente")

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
                confirmacion = False
                while not confirmacion:
                    try:
                        horas = estadia // 60
                        minutos = estadia % 60
                        horas_s = 'una hora' if horas == 1 else f'{
                            horas} horas'
                        minutos_s = 'un minuto' if minutos == 1 else f'{
                            minutos} minutos'
                        mensaje = f"Entendí {horas_s} {
                            minutos_s} ¿Es esto correcto?"
                        confirmacion = entrada.obtener_confirmacion(mensaje)
                        if not confirmacion:
                            entrada.informar_mensaje(
                                "Por favor vuelva a indicar su estadia"
                            )
                            estadia_ok = False
                            confirmacion = True
                        else:
                            entrada.informar_mensaje(
                                f"Estadia de {estadia} minutos confirmada!"
                            )
                    except ConfirmacionProcesamientoException:
                        entrada.informar_mensaje(
                            "No se pudo procesar la confirmacion, intente nuevamente"
                        )

            except EstadiaProcesamientoException:
                entrada.informar_mensaje(
                    "No se pudo procesar la estadia, intente nuevamente"
                )

        techado = True
        while True:
            try:
                techado = entrada.obtener_confirmacion(
                    "¿Prefiere que su estacionamiento sea techado?")
                break
            except ConfirmacionProcesamientoException:
                entrada.informar_mensaje(
                    "No se pudo procesar la respuesta, intente nuevamente"
                )

        reserva = entrada.verificar_espacios(patente, estadia, techado)

        if reserva:
            entrada.permitir_estacionar(reserva)
        else:
            entrada.informar_mensaje(
                "No hay espacio disponible, retire su vehiculo por favor"
            )
