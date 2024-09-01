from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet,  ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime

def draw_vertical_line(c, doc):
    """Draw a vertical line on the canvas to separate the logos."""
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    line_x = 205  # X position for the vertical line
    line_y_start = A4[1] - 55  # Start Y position (top of the page)
    line_y_end = A4[1] - 20  # End Y position (a bit lower)
    c.line(line_x, line_y_start, line_x, line_y_end)

def create_pdf_report(filename:str, usuario:str, last_digits:str, producto: str,start_date: datetime, end_date: datetime, kpis: list, registers: list):

    # Create a SimpleDocTemplate
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            leftMargin=0,
                            rightMargin=0,
                            topMargin=0,
                            bottomMargin=0)

    # Create a Story list to hold the elements
    Story = []
    
    # Register the Cormorant Garamond Bold font
    cormorant_font_path = "resources\\CormorantGaramond-Bold.ttf"  # Replace with your font path
    pdfmetrics.registerFont(TTFont('CormorantGaramondBold', cormorant_font_path))

    # Register the Cormorant Garamond font
    cormorant_font_path = "resources\\CormorantGaramond-Regular.ttf"  # Replace with your font path
    pdfmetrics.registerFont(TTFont('CormorantGaramond', cormorant_font_path))

    styles = getSampleStyleSheet()

    style_logo = ParagraphStyle(
        'Custom_logo',
        parent=styles['Normal'],  # Inherit properties from 'Normal' style
        fontName='CormorantGaramondBold',  # Use the registered custom font
        fontSize=16,  # Set the font size to 16
        alignment=0,  # Align text to the left
    )


    # Load the images and add them to the story
    left_logo_path = "resources\\Logo_S&S_Black_Circle.png"  # Replace with your logo path
    right_logo_path = "resources\\Bybit.png"  # Replace with your logo path
    left_logo = Image(left_logo_path, width=60, height=45)
    right_logo = Image(right_logo_path, width=105, height=55)

    # Create a table for side-by-side images and text
    table_data = [
        [left_logo, Paragraph("S&amp;S Investments", style_logo), right_logo]
    ]
    table = Table(table_data, colWidths=[70, 125, 120], hAlign='LEFT')

    # Define the table style for alignment
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all contents to the center
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),    # Align the left logo to the left
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Center align the text
        ('ALIGN', (2, 0), (2, 0), 'LEFT'),    # Align the right logo to the right
        ('BOTTOMPADDING', (1, 0), (1, 0), 12),
    ]))

    # Add the table to the story
    Story.append(table)
    Story.append(Spacer(1, 20))  # Add space below the table

    # Add name of the person who requested the report
    general_info = [
        ["Señor (a):", usuario],
        ["Cuenta: ", f"*****{last_digits}"],
        ["Producto: ", producto],
    ]
    table_general_info = Table(general_info, colWidths=[50, 50], hAlign='LEFT')

    table_general_info.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'CormorantGaramond'),
        ('FONTNAME', (1, 0), (1, -1), 'CormorantGaramondBold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ]))

    # Define the data for the table
    data_date = [
        ["Periodo de Reporte"],
        ['Desde', 'Hasta'],
        [start_date.strftime("%m/%d/%Y"), end_date.strftime("%m/%d/%Y")],
    ]

    # Create a Table object with the specified column widths
    table_date = Table(data_date, colWidths=170,)

    # Set the style for the table
    table_date.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),  # Merge the first row
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Lighter grey for the first row
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center all text
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center all text
        ('FONTNAME', (0, 0), (-1, 0), 'CormorantGaramondBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),  # Set font size for the first row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (2, 0), (2, -1), 2),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'CormorantGaramond')
    ])) 

    # Create Parent Table
    parent_table_data = [[table_general_info, table_date]]
    parent_table = Table(parent_table_data)
    parent_table.setStyle(TableStyle([
    ('LEFTPADDING', (0, 1), (0, 1), 30),  # Padding left for the second table
    ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),  # Vertically center the first cell
]))

    # Add the table to the Story
    Story.append(parent_table)
    Story.append(Spacer(1, 20))  # Add space below the table

    
    # Create table of KPIs
    if kpis is not None and len(kpis) == 4:
        data_kpi = [
            ["Saldo Inicial", "Saldo Final", "Balance Total", "Tasa Mensual Efectiva (M.E)"],
            [kpis[0], kpis[1], kpis[2], kpis[3]],
        ]
    else:
        data_kpi = [
            ["Saldo Inicial", "Saldo Final", "Balance Total", "Tasa Mensual Efectiva (M.E)"],
            ["N/A", "N/A", "N/A", "N/A"],
        ]

    # Create a Table object for KPIs with the specified column widths and row heights
    table_kpi = Table(data_kpi, colWidths=[142, 142, 142, 142], rowHeights=20)

    # Apply the same style to the KPI table
    table_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Lighter grey for the first row
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center all text
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center all text
        ('FONTNAME', (0, 0), (-1, 0), 'CormorantGaramondBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Set font size for the first row
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'CormorantGaramond')
    ])) 

    # Add the KPI table to the Story
    Story.append(Spacer(1, 12))
    Story.append(table_kpi)
    Story.append(Spacer(1, 12))

    # Create table of registers
    data_registers = [
        ["Id", "Fecha", "Cantidad", "Profit", "Aporte"]
    ]

    for register in registers:
        data_registers.append([register["Id"], register["Fecha"], register["Cantidad"], register["Profit"], f"{register['Aporte']}%"])

    table_registers = Table(data_registers, colWidths=[195, 150, 74, 74, 75], rowHeights=20)
    table_registers.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Lighter grey for the first row
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center all text
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center all text
        ('FONTNAME', (0, 0), (-1, 0), 'CormorantGaramondBold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Set font size for the first row
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'CormorantGaramond')
    ])) 

    # Add the registers table to the Story
    Story.append(table_registers)

    # Build the PDF document
    doc.build(Story, onFirstPage=draw_vertical_line)