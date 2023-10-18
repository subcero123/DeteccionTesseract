from __future__ import print_function

# Updating the system path is not required if you have pip-installed
# rticonnextdds-connector
from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
    config_name="MyParticipantLibrary::MySubParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    input = connector.get_input("MySubscriber::MyTextReader")

    print("Waiting for publications...")
    input.wait_for_publications()  # Espera al menos una publicación coincidente

    print("Waiting for data...")
    for i in range(1, 500):
        input.wait()  # Espera datos en esta entrada
        input.take()
        for sample in input.samples.valid_data_iter:
            # Obtén el campo 'texto' del mensaje
            texto_recibido = sample.get_string("texto")
            print("Texto recibido: " + texto_recibido)
