from __future__ import print_function

from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
    config_name="MyParticipantLibrary::PostProcessorParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    input = connector.get_input("PostProcessorSubscriber::PostProcessorReader")
    output = connector.get_output("PostProcessorPublisher::PostProcessorWriter")

    print("Waiting for subscriptions...")
    input.wait_for_publications()

    print("Waiting for recognized text...")
    for i in range(1, 500):
        input.wait()
        input.take()
        for sample in input.samples.valid_data_iter:
            texto_recibido = sample.get_string("texto")
            # Realiza el postprocesamiento en texto_recibido
            texto_procesado = "Texto procesado para " + texto_recibido

            # Publica el texto procesado nuevamente en el tema de segmentación
            output.instance.set_string("segment", texto_procesado)
            output.write()
