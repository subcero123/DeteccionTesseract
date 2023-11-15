import os
from time import sleep
import rticonnextdds_connector as rti
from sys import path as sys_path
from os import path as os_path
from OCRfinal import *

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

# Directorio donde se encuentran los archivos PDF
pdf_directory = 'PDF'

# Obtener la lista de archivos PDF en el directorio
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

with rti.open_connector(
    config_name="MyParticipantLibrary::MyPubParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    output = connector.get_output("MyPublisher::MyTextPublisher")

    print("Waiting for subscriptions...")
    output.wait_for_subscriptions()

    for pdf_filename in pdf_files:
        pdf_filepath = os.path.join(pdf_directory, pdf_filename)
        parrafo = obtenerParrafo(pdf_filepath)
        parrafo = " ".join(parrafo)

        print(f"Writing content from {pdf_filename}...")

        max_length = 9000  # Nueva longitud máxima

        text_fragments = [parrafo[i:i + max_length] for i in range(0, len(parrafo), max_length)]

        for fragment in text_fragments:
            recognized_text = fragment  # Aquí defines el fragmento de texto
            output.instance.set_string("texto", recognized_text)
            output.write()
            sleep(0.5)  # Escribe a una velocidad de un mensaje cada 0.5 segundos

    print("Exiting...")
    output.wait()  # Espera a que todas las suscripciones reciban los datos antes de salir
