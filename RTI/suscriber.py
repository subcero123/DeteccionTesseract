#Responsable de unir el PDF
from __future__ import print_function

from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
    config_name="MyParticipantLibrary::PDFGeneratorParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    input = connector.get_input("PDFGeneratorSubscriber::PDFGeneratorReader")

    print("Waiting for subscriptions...")
    input.wait_for_publications()

    print("Waiting for processed text...")
    for i in range(1, 500):
        input.wait()
        input.take()
        for sample in input.samples.valid_data_iter:
            segmento_recibido = sample.get_string("segment")
            # Realiza la generación de PDF con segmento_recibido
            # Puedes utilizar bibliotecas como PyPDF2 o ReportLab para esto
