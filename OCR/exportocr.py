from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ocr import texto
pdf_file = "informacionOCR.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
c.setFont("Helvetica", 12)
text_object = c.beginText(100, 750) 
text_object.textLines(texto)
c.drawText(text_object)
c.save()
