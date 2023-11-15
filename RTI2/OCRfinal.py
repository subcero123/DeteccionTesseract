# Importación de bibliotecas necesarias
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
import spacy
from fpdf import FPDF

# Función para abrir un archivo PDF
def open_pdf(pdf_filename):
    return PdfReader(open(pdf_filename, 'rb'))

# Función para determinar si una imagen contiene texto
def is_image_containing_text(image):
    # Convierte la imagen en escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplica un umbral para binarizar la imagen
    _, thresholded = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    # Encuentra contornos en la imagen binarizada
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Devuelve True si se encontraron contornos (texto), de lo contrario, False
    return len(contours) > 0

# Función para extraer texto de una imagen
def extract_text_from_image(image, nlp):
    # Convierte la imagen en un formato adecuado para OCR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Utiliza Tesseract para extraer texto de la imagen
    image_text = pytesseract.image_to_string(image)
    # Procesa el texto extraído con spaCy para mejorar la calidad
    doc = nlp(image_text)
    improved_image_text = ' '.join([token.text if not token.is_stop else '' for token in doc])
    return improved_image_text

# Función principal para procesar el PDF y generar un PDF mejorado
def process_pdf(pdf_filename, nlp):
    # Abre el archivo PDF
    pdf_reader = open_pdf(pdf_filename)
    improved_text = ""
    page_number = 0

    # Itera a través de las páginas del PDF
    for page in pdf_reader.pages:
        page_number += 1
        pdf_text = page.extract_text()
        images = convert_from_path(pdf_filename, first_page=page_number, last_page=page_number)

        if images:
            image = np.array(images[0])
            if is_image_containing_text(image):
                content_status = "Contiene texto extraído de una imagen"
                improved_image_text = extract_text_from_image(image, nlp)
                improved_text += f'{pdf_text}\n{improved_image_text}\n'
            else:
                content_status = "No contiene texto extraído de una imagen"
                improved_text += pdf_text
        else:
            content_status = "Contiene texto extraído directamente del PDF"
            improved_text += pdf_text

    # Divide el texto en párrafos
    paragraphs = improved_text.split('\n')
    return paragraphs

# Clase personalizada que hereda de FPDF para generar un PDF mejorado
class ImprovedPDF(FPDF):
    def add_improved_text(self, paragraphs, nlp, interlineado=5):
        self.add_page()
        self.set_font("Arial", size=12)
        for paragraph in paragraphs:
            self.multi_cell(0, 10, paragraph)
            self.ln(interlineado)  # Agrega interlineado después de cada párrafo

    def generate_improved_pdf(self, output_filename):
        self.output(output_filename)

# Función principal que coordina el proceso
def obtenerParrafo(pdf_filename):
    # Carga el modelo de lenguaje de spaCy
    nlp = spacy.load('es_core_news_sm')
    # Procesa el PDF y obtiene los párrafos mejorados
    paragraphs = process_pdf(pdf_filename, nlp)
    return paragraphs

def generarOutput(paragraphs, output_filename):
    # Crea un objeto ImprovedPDF y genera el PDF mejorado
    pdf = ImprovedPDF()
    pdf.add_improved_text(paragraphs, None)  # No se utiliza spaCy para identificar títulos o subtítulos
    pdf.generate_improved_pdf(output_filename)
    print(f'El PDF mejorado se ha guardado como "{output_filename}"')

if __name__ == "__main__":
    # Nombre del archivo PDF de entrada y nombre del archivo de salida
    pdf_filename = 'Res.pdf'
    output_filename = 'textomejorado.pdf'
    # Llama a la función principal para iniciar el proceso
    paragraphs = obtenerParrafo(pdf_filename)
    generarOutput(paragraphs, output_filename)