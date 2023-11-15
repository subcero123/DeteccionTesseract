#Encargado de publicar-suscribir reconocimiento
from __future__ import print_function

from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
    config_name="MyParticipantLibrary::RecognizerParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    input = connector.get_input("RecognizerSubscriber::RecognizerReader")
    output = connector.get_output("RecognizerPublisher::RecognizerWriter")

    print("Waiting for subscriptions...")
    input.wait_for_publications()

    print("Waiting for segmented text...")
    for i in range(1, 500):
        input.wait()
        input.take()
        for sample in input.samples.valid_data_iter:
            segmento_recibido = sample.get_string("segment")
            # Realiza el proceso de OCR en segmento_recibido y obtén el texto reconocido
            texto_reconocido = "Texto reconocido para " + segmento_recibido

            # Publica el texto reconocido
            output.instance.set_string("texto", texto_reconocido)
            output.write()
