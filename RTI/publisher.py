from time import sleep

# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
    config_name="MyParticipantLibrary::MyPubParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    output = connector.get_output("MyPublisher::MyTextPublisher")

    print("Waiting for subscriptions...")
    output.wait_for_subscriptions()

    print("Writing...")
    for i in range(1, 10):
        recognized_text = "Texto reconocido..."  # Aquí define el texto que deseas enviar
        output.instance.set_string("texto", recognized_text)
        output.write()

        sleep(0.5)  # Escribe a una velocidad de un mensaje cada 0.5 segundos, por ejemplo.

    print("Exiting...")
    output.wait()  # Espera a que todas las suscripciones reciban los datos antes de salir
