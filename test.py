import RPi.GPIO as GPIO
from datetime import datetime
import requests
import time

PARKING_ID = 1
BEAM_PIN_ENTRADA = 27
BEAM_PIN_SORTIDA = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN_ENTRADA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BEAM_PIN_SORTIDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    last_entrada = 1
    last_sortida = 1
    while True:
        if GPIO.input(BEAM_PIN_ENTRADA) == 0:
            print("Ha passat un cotxe")
            if last_entrada == 1:
                print("Enviar a API entrada")
                print(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
                requests.post(
                    url="http://localhost:80/event/insert",
                    json={
                        "parking_id": PARKING_ID,
                        "event_type": "ENTRY",
                        "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    },
                    headers={"Content-Type": "application/json"}
                )
        if GPIO.input(BEAM_PIN_SORTIDA) == 0:
            print("Ha sortit un cotxe")
            if last_sortida == 1:
                print("Enviar a API sortida")
                requests.post(
                    url="http://localhost:80/event/insert",
                    json={
                        "parking_id": PARKING_ID,
                        "event_type": "EXIT",
                        "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    },
                    headers={"Content-Type": "application/json"}
                )
        last_entrada = GPIO.input(BEAM_PIN_ENTRADA)
        last_sortida = GPIO.input(BEAM_PIN_SORTIDA)
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
