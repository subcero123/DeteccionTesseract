from time import sleep
import rticonnextdds_connector as rti
from sys import path as sys_path
from os import path as os_path
from OCRfinal import *

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

# Abrir el archivo PDF y leer su contenido binario
with open('../aPdf/1.pdf', 'rb') as pdf_file:
    pdf_content = pdf_file.read()

with rti.open_connector(
    config_name="MyParticipantLibrary::MyPubParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    output = connector.get_output("MyPublisher::MyTextPublisher")

    print("Waiting for subscriptions...")
    output.wait_for_subscriptions()

    pdf_filename = '1.pdf'
    parrafo = obtenerParrafo(pdf_filename)
    parrafo = " ".join(parrafo)

    print("Writing...")
    for i in range(1, 2):
        recognized_text = parrafo  # Aquí define el texto que deseas enviar
        output.instance.set_string("texto", recognized_text)
        output.write()

        sleep(0.5)  # Escribe a una velocidad de un mensaje cada 0.5 segundos, por ejemplo.

    print("Exiting...")
    output.wait()  # Espera a que todas las suscripciones reciban los datos antes de salir