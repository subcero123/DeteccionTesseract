import PyPDF2
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np  # Añade esta importación
import spacy
from fpdf import FPDF

# Abre el archivo PDF en modo lectura binaria
pdf_filename = '1.pdf'  # Reemplaza con la ruta de tu PDF
pdf_reader = PyPDF2.PdfReader(open(pdf_filename, 'rb'))

# Función para verificar si una imagen contiene texto
def is_image_containing_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        return True
    else:
        return False

# Variables para almacenar el contenido mejorado
improved_text = ""
page_number = 0  # Variable para rastrear el número de página

# Configura spaCy para el procesamiento de lenguaje natural
nlp = spacy.load('es_core_news_sm')  # Reemplaza 'es' con el idioma de tu elección

# Lee el PDF y verifica si cada página contiene texto o imágenes
for page in pdf_reader.pages:
    page_number += 1
    pdf_text = page.extract_text()

    images = convert_from_path(pdf_filename, first_page=page_number, last_page=page_number)

    if images:
        # Si la página se convierte en una imagen, verifica si contiene texto
        image = np.array(images[0])  # Convierte la imagen en un arreglo numpy
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if is_image_containing_text(image):
            content_status = "Contiene texto extraído de una imagen"
            image_text = pytesseract.image_to_string(image)

            # Aplica NLP al texto de la imagen
            doc = nlp(image_text)
            improved_image_text = ' '.join([token.text if not token.is_stop else '' for token in doc])

            improved_text += f'{pdf_text}\n{improved_image_text}\n'
        else:
            content_status = "No contiene texto extraído de una imagen"
            improved_text += pdf_text
    else:
        content_status = "Contiene texto extraído directamente del PDF"
        improved_text += pdf_text

    print(f'Procesando página {page_number}...')

print("Procesamiento de NLP en PDF completado.")

# Generar un nuevo PDF con el texto mejorado
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Texto Mejorado', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, improved_text)

pdf_filename_output = 'texto_mejorado.pdf'
pdf.output(pdf_filename_output)

print("Texto Mejorado:")
print(improved_text)
print(f'El PDF mejorado se ha guardado como "{pdf_filename_output}"')

