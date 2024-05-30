from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def info_pdf(story):
    
    # Crear una tabla de 5x3
    data = [
        ['Celda 1,1', 'Celda 1,2', 'Celda 1,3'],
        ['Celda 2,1', 'Celda 2,2', 'Celda 2,3'],
        ['Celda 3,1', 'Celda 3,2', 'Celda 3,3'],
        ['Celda 4,1', 'Celda 4,2', 'Celda 4,3'],
        ['Celda 5,1', 'Celda 5,2', 'Celda 5,3']
    ]
    
    table = Table(data, colWidths=[2 * inch] * 3, rowHeights=[0.6 * inch] * 5)
    
    # Aplicar estilo a la tabla
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ('LINEBEFORE', (0, 0), (0, -1), 0.5, colors.black),
        ('LINEAFTER', (-1, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(style)
    
    
    story.append(table)



pdf_path = "prueba1.pdf"

margin = 0.1 * inch
    
doc = SimpleDocTemplate(
    pdf_path, 
    pagesize=letter,
    rightMargin=margin,
    leftMargin=margin,
    topMargin=margin,
    bottomMargin=margin
)

# Crear una lista para almacenar los elementos
story = []

info_pdf(story)
    
doc.title = "Informe Anual"

doc.build(story)


