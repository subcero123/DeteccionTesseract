#Encargado de la segmentacion del texto
#Orden de ejecución, publisher, reconocimiento, postprocesamiento, suscriber. 
from time import sleep

from sys import path as sys_path
from os import path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))
sys_path.append(file_path + "/../../../")

import rticonnextdds_connector as rti

with rti.open_connector(
    config_name="MyParticipantLibrary::SegmenterParticipant",
    url=file_path + "/MyAppConfig.xml"
) as connector:

    output = connector.get_output("SegmenterPublisher::SegmenterWriter")

    print("Waiting for subscribers...")
    output.wait_for_subscriptions()

    print("Writing segmented text...")
    segmented_texts = ["Segment 1 of text...", "Segment 2 of text...", "Segment 3 of text..."]

    for segment in segmented_texts:
        output.instance.set_string("segment", segment)
        output.write()

        sleep(0.5)
