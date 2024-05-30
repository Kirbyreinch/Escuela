from peewee import fn

from Pages.escuelas import consult_escuelas

from fastapi import HTTPException

from database import Supervisor, Escuela, Reports, Income, Expenses, User_Info

from peewee import DoesNotExist

#region reportlab imports
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
#endregion

def format_currency(value):
    
    return f"${value:,.2f}"

async def get_supervisor(id):

    supervisor = Supervisor.get_by_id(id)
    
    return supervisor

async def get_number_report(school: str):

    if not Escuela.select().where((Escuela.nombre == school) & (Escuela.activate == True)).exists():
        raise HTTPException(status_code=400, detail="La escuela no existe")
    
    ultimo_reporte = Reports.select().where(Reports.escuela == school).order_by(Reports.numero_reporte.desc()).first()
    
    if ultimo_reporte:
        return ultimo_reporte.numero_reporte + 1
    else:
        return 1

async def get_all_incomes_with_date(school:str, start_year, end_year):
    
    if not Income.select().where(Income.school_name == school).exists():
        raise HTTPException(status_code=400, detail="No existen ingresos de la escuela")
    
    start_year = int(start_year)
    end_year = int(end_year)
    
    income_info = (Income.select(Income.category, Income.otros_especificar, Income.amount).where((Income.school_name == school) & (fn.YEAR(Income.date) >= start_year) & (fn.YEAR(Income.date) <= end_year)).order_by(Income.id.desc()))    

    school_info_list = []
    school_info_list_other = []

    for income in income_info:

        if income.category == "otros":
            
            school_info_list_other.append({

                "other": income.otros_especificar,
                "amount": income.amount,

            })
        
        else:

            school_info_list.append({

                "category": income.category,
                "amount": income.amount,

            })
            
            
    return school_info_list, school_info_list_other

async def get_all_expenses_with_date(school:str, start_year:str, end_year:str):
    
    if not Income.select().where(Income.school_name == school).exists():
        raise HTTPException(status_code=400, detail="No existen ingresos de la escuela")
    
    start_year = int(start_year)
    end_year = int(end_year)
    
    school_info_list = []
    school_info_list_other = []
    
    expense_info = (Expenses.select(Expenses.category, Expenses.monto).where((Expenses.escuela_nombre == school) & (fn.YEAR(Expenses.fecha) >= start_year) & (fn.YEAR(Expenses.fecha) <= end_year)).order_by(Expenses.id.desc()))    
    
    for expense in expense_info:

        if expense.category == "otros":
            
            school_info_list_other.append({

                "other": expense.category,
                "amount": expense.monto,

            })
        
        else:

            school_info_list.append({

                "category": expense.category,
                "amount": expense.monto,

            })
            
            
    return school_info_list, school_info_list_other

async def get_school_names(school:str):
    
    if not Escuela.select().where(Escuela.nombre == school).exists():
        raise HTTPException(status_code=400, detail="La escuela no existe")
    
    
    try:
            escuela = Escuela.get(Escuela.nombre == school)

            presidente_info = User_Info.get(User_Info.user_id == escuela.presidente_id)
            director_info = User_Info.get(User_Info.user_id == escuela.director_id)
            tesorero_info = User_Info.get(User_Info.user_id == escuela.tesorero_id)

            school_list = [{
                "presidente": f"{presidente_info.name} {presidente_info.last_name}",
                "director": f"{director_info.name} {director_info.last_name}",
                "tesorero": f"{tesorero_info.name} {tesorero_info.last_name}"
            }]
            
            return school_list

    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Información de usuario no encontrada")



async def create_pdf(pdf_request):
    
    #region styles
    styles = getSampleStyleSheet()

    title_standard = ParagraphStyle(
        "title_standard",                
        fontSize=12,                   
        alignment=1,                   
        fontName="Times-Roman",
        leading=15,
    )
    
    title_bold = ParagraphStyle(
        "title_bold",
        fontSize=12,                   
        alignment=1,                   
        fontName="Times-Bold",
        leading=15,
    )
    
    title_bold_records = ParagraphStyle(
        "title_bold_records",
        fontSize=11,                   
        alignment=0,                   
        fontName="Times-Bold",
        leading=15,
    )
    
    title_bold_amounts = ParagraphStyle(
        "title_bold_amounts",
        fontSize=11,                   
        alignment=2,                   
        fontName="Times-Bold",
    )
    
    title_normal_amounts = ParagraphStyle(
        "title_normal_amounts",
        fontSize=11,                   
        alignment=2,                   
        fontName="Times-Roman",
    )
    
    # Agregar el nuevo estilo al diccionario de estilos
    styles.add(title_standard)
    styles.add(title_bold)
    styles.add(title_bold_records)
    styles.add(title_bold_amounts)
    styles.add(title_normal_amounts)
    
    #endregion
    
    info_names = await get_school_names(pdf_request.school)
    incomes, other_incomes = await get_all_incomes_with_date(pdf_request.school, pdf_request.start_year, pdf_request.end_year)
    expenses, other_expenses = await get_all_expenses_with_date(pdf_request.school, pdf_request.start_year, pdf_request.end_year)
    
    num_reporte = await get_number_report(pdf_request.school)
    supervisor = await get_supervisor(pdf_request.id)
    info_school = await consult_escuelas(pdf_request.school)
    
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

    titles_pdf(story, styles, supervisor.estado, num_reporte, pdf_request.start_year, pdf_request.end_year)
    
    info_pdf(story, info_school)
    
    tt_ingreso = incomes_pdf(story, styles, incomes, other_incomes)
    
    tt_egreso = expenses_pdf(story, styles, expenses, other_expenses)
    
    final_amount_pdf(story, tt_ingreso, tt_egreso)
    
    signature_section_pdf(story, styles, info_names)

    
    doc.title = "Informe Anual"
    doc.build(story)
    
def titles_pdf(story, styles, estado:str, num_reporte:int, start_date:str, end_date:str):

    # Textos
    text1 = Paragraph(f"GOBIERNO DEL ESTADO DE {estado.upper()}", styles['title_bold'])
    text2 = Paragraph("SECRETARÍA DE EDUCACIÓN PUBLICA Y CULTURA", styles['title_standard'])
    text3 = Paragraph("DIRECCIÓN DE VINCULACIÓN SOCIAL", styles['title_standard'])

    # Lista de párrafos
    text = [text1, text2, text3]

    # Imagen
    img_path = 'logo.PNG'
    img_width = 2 * inch  # Ajusta el ancho de la imagen
    img_height = 0.8 * inch  # Ajusta el alto de la imagen
    img = Image(img_path, width=img_width, height=img_height)

    # Crear una tabla con 1 fila y 2 columnas
    data = [[img, text]]
    table = Table(data, colWidths=[img_width, 6 * inch], rowHeights=[img_height])

    # Estilo de la tabla
    style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Alinear imagen al centro
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # Centrar verticalmente la imagen
        ('ALIGN', (1, 0), (1, 2), 'RIGHT'),  # Alinear texto a la derecha
        ('VALIGN', (1, 0), (1, 2), 'MIDDLE'),  # Centrar verticalmente el texto
    ])

    table.setStyle(style)
    
    # Añadir la tabla al story
    story.append(table)

    text4 = Paragraph("COORDINACIÓN ESTATAL DE UNIDADES DE ATENCIÓN A PADRES DE FAMILIA", styles['title_standard'])
    story.append(text4)
    
    story.append(Spacer(1, 5))
    
    text5 = Paragraph(f"{num_reporte}° Informe Financiero de las Asociaciones de Padres de Familia", styles['title_bold']) 
    story.append(text5)
    
    text6 = Paragraph(f"Ciclo escolar {start_date} - {end_date}", styles['title_standard']) 
    story.append(text6)
    
def info_pdf(story, info_school):

    cuota_format = format_currency(info_school.get("cuota", 0))  
    
    # Crear una tabla de 5x3
    data = [
        ['Escuela',                                                 f'Clave: {info_school["clave"]} ',       f'Turno: {info_school["turno"]}'],
        [f'Zona:                    {info_school["zona"]}',         f'Sector: {info_school["sector"]}',      f'Domicilio: {info_school["domicilio"]}'],
        [f'Localidad:               {info_school["localidad"]}',    f'Telefono: {info_school["telefono"]}',  ''],
        [f'No. de Padre de Familia: {info_school["no_familia"]}',   '',                                      f'Cuota de Padres de Familia: {cuota_format}'],
        [f'Total de Alumnos:        {info_school["tt_alumnos"]}',   '',                                      f'Total de Grupos: {info_school["tt_grupos"]}']
    ]
    
    table = Table(data, colWidths=[2.5 * inch] * 3, rowHeights=[0.3 * inch] * 5)
    
    story.append(Spacer(2, 10))
    
    style = TableStyle([
        # Alineación: primera columna a la izquierda, segunda en el centro, tercera a la derecha
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        # Verticalmente alineado hacia arriba solo en la primera fila
        ('VALIGN', (0, 0), (-1, 0), 'TOP'),
        # Fuente y tamaño de fuente
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        # Estilo de bordes
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ('LINEBEFORE', (0, 0), (0, -1), 0.5, colors.black),
        ('LINEAFTER', (-1, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(style)
    
    story.append(table)

def incomes_pdf(story, styles, incomes, other_incomes):
    
    tt_incomes = sum(income['amount'] for income in incomes)
    tt_other_incomes = sum(income['amount'] for income in other_incomes)
    
    # Crear datos de la tabla de ingresos dinámicamente
    data = [[Paragraph('A. INGRESOS ECONÓMICOS.', styles['title_bold_records'])]]
    
    data.append(['TOTAL DE INGRESOS PRIMER PERIODO'])
    
    for ingreso in incomes:
        data.append([ingreso['category'], format_currency(ingreso['amount'])])
    
    data.append(['Otros ingresos (especifique): '])
    
    for other in other_incomes:
            data.append([other['other'], format_currency(other['amount'])])
    
    data.append([
        Paragraph('TOTAL DE INGRESOS:', styles['title_bold_amounts']),
        Paragraph(format_currency(tt_incomes + tt_other_incomes), styles['title_normal_amounts'])
    ])
    
    # Crear una tabla con tantas filas como ingresos haya
    table = Table(data, colWidths=[5.5 * inch, 2 * inch], rowHeights=[0.2 * inch] * len(data))
    
    story.append(Spacer(2, 10))
    
    style = TableStyle([
        # Alineación
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        # Fuente y tamaño de fuente
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        # Estilo de bordes y fondos
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ('LINEBEFORE', (0, 0), (0, -1), 0.5, colors.black),
        ('LINEAFTER', (-1, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(style)
    
    story.append(table)
    
    return tt_incomes + tt_other_incomes
    
def expenses_pdf(story, styles, expenses, other_expenses):
    
    tt_expense = sum(expense['amount'] for expense in expenses)
    tt_other_expense = sum(expense['amount'] for expense in other_expenses)
    
    # Crear datos de la tabla de ingresos dinámicamente
    data = [[Paragraph('B. EGRESOS REGISTRADOS', styles['title_bold_records'])]]
    data.append(['TOTAL DE EGRESOS PRIMER PERIODO'])
    
    for egreso in expenses:
        data.append([egreso['category'], format_currency(egreso['amount'])])
    
    data.append(['Otros', format_currency(tt_other_expense)])
    
    data.append([
        Paragraph('TOTAL DE EGRESOS:', styles['title_bold_amounts']),
        Paragraph(format_currency(tt_expense + tt_other_expense), styles['title_normal_amounts'])
    ])
    

    # Crear una tabla con tantas filas como ingresos haya
    table = Table(data, colWidths=[5.5 * inch, 2 * inch], rowHeights=[0.2 * inch] * len(data))
    
    story.append(Spacer(2, 10))
    
    style = TableStyle([
        # Alineación
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        # Fuente y tamaño de fuente
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        # Estilo de bordes y fondos
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
        ('LINEBEFORE', (0, 0), (0, -1), 0.5, colors.black),
        ('LINEAFTER', (-1, 0), (-1, -1), 0.5, colors.black),
    ])
    table.setStyle(style)
    
    story.append(table)
    
    return tt_expense + tt_other_expense
    
def final_amount_pdf(story, tt_ingresos: float, tt_egresos: float):
    
    saldo = tt_ingresos - tt_egresos
    
    # Datos para la tabla de 1x1
    data = [['Saldo', format_currency(saldo)]]
    
    # Crear una tabla de 1x1
    table = Table(data, colWidths=[5.5 * inch, 2 * inch], rowHeights=[0.5 * inch])

    # Estilos de la tabla
    style = TableStyle([
        ('ALIGN', (0, 0), (-2, -1), 'RIGHT'),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ])
    table.setStyle(style)
    
    # Añadir la tabla al Story
    story.append(table)

def signature_section_pdf(story, styles, info_names):

    print(info_names[0]['presidente'])
    presidente = info_names[0]['presidente']
    
    data = [
        [Paragraph('Fecha: ', styles['Normal']), Paragraph('', styles['Normal'])],
        [Paragraph('____________________', styles['Normal']), Paragraph('____________________', styles['Normal'])],
        [Paragraph( presidente, styles['Normal']), Paragraph('Row 2, Col 2', styles['Normal'])],
        [Paragraph('PRESIDENTE DE LA MESA DIRECTIVA', styles['Normal']), Paragraph('TESORERO DE LA MESA DIRECTIVA', styles['Normal'])],
        [Paragraph('', styles['Normal']), Paragraph('', styles['Normal'])],
        [Paragraph('____________________', styles['Normal']), Paragraph('____________________', styles['Normal'])],
        [Paragraph('Row 6, Col 1', styles['Normal']), Paragraph('Row 6, Col 2', styles['Normal'])],
        [Paragraph('VoBo DIRECTOR', styles['Normal']), Paragraph('VoBo SUPERVISOR ESCOLAR 018', styles['Normal'])],
    ]

    # Crear la tabla
    table = Table(data, colWidths=[3 * inch, 3 * inch], rowHeights=[0.5 * inch] * 8)

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Times-Bold'), # Primera columna en negrita
        ('FONTNAME', (1, 0), (1, -1), 'Times-Roman'), # Segunda columna en Times-Roman
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
    ])
    table.setStyle(style)

    # Añadir la tabla al Story
    story.append(table)
