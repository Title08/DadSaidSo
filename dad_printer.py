"""
DadSaidSo - PDF Generator Module
Creates professional quotation PDFs with Thai language support
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bahttext import bahttext

# Load environment variables
load_dotenv()

# Load environment variables
load_dotenv()


# ==========================================
# CONFIGURATION
# ==========================================

# Company Information from .env
COMPANY_NAME = os.getenv("COMPANY_NAME", "ชื่อบริษัท/ร้านค้า ของคุณ")
COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS", "ที่อยู่ของคุณ ต.ตำบล อ.อำเภอ จ.จังหวัด 00000")
COMPANY_PHONE = os.getenv("COMPANY_PHONE", "08x-xxxxxxx")
COMPANY_TAX_ID = os.getenv("COMPANY_TAX_ID", "0000000000000")
QUOTER_FIRSTNAME = os.getenv("QUOTER_FIRSTNAME", "ชื่อ")
QUOTER_LASTNAME = os.getenv("QUOTER_LASTNAME", "นามสกุล")


# ==========================================
# FONT CONFIGURATION
# ==========================================

def get_font_path(filename):
    """Get absolute path to font file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fonts', filename)


def register_thai_fonts():
    """
    Register Thai fonts (TH Sarabun New)
    Falls back to Helvetica if fonts are not available
    
    Returns:
        dict: Font mapping with keys: 'main', 'bold', 'title'
    """
    font_files = {
        'regular': get_font_path('THSarabunNew.ttf'),
        'bold': get_font_path('THSarabunNew Bold.ttf'),
        'italic': get_font_path('THSarabunNew Italic.ttf'),
        'bold_italic': get_font_path('THSarabunNew BoldItalic.ttf')
    }
    
    # Default fallback fonts
    font_map = {
        'main': 'Helvetica',
        'bold': 'Helvetica-Bold',
        'title': 'Helvetica-Bold'
    }
    
    # Try to register main font
    if os.path.exists(font_files['regular']):
        pdfmetrics.registerFont(TTFont('THSarabunNew', font_files['regular']))
        font_map['main'] = 'THSarabunNew'
    elif os.path.exists('THSarabunNew.ttf'):  # Try local directory
        pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))
        font_map['main'] = 'THSarabunNew'
    else:
        print("⚠️  Thai font not found, using Helvetica")
        return font_map
    
    # Register bold font
    if os.path.exists(font_files['bold']):
        pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', font_files['bold']))
        font_map['bold'] = 'THSarabunNew-Bold'
    else:
        # Fallback: use regular font for bold
        from reportlab.lib.fonts import addMapping
        addMapping('THSarabunNew', 1, 0, 'THSarabunNew')
        font_map['bold'] = 'THSarabunNew'
    
    # Register title font (bold italic if available, else bold)
    if os.path.exists(font_files['bold_italic']):
        pdfmetrics.registerFont(TTFont('THSarabunNew-BoldItalic', font_files['bold_italic']))
        font_map['title'] = 'THSarabunNew-BoldItalic'
    else:
        font_map['title'] = font_map['bold']
    
    # Register italic font (optional)
    if os.path.exists(font_files['italic']):
        pdfmetrics.registerFont(TTFont('THSarabunNew-Italic', font_files['italic']))
    
    return font_map


# ==========================================
# STYLE CONFIGURATION
# ==========================================

def create_styles(font_map):
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()
    
    custom_styles = {
        'normal': ParagraphStyle(
            name='ThaiNormal',
            parent=styles['Normal'],
            fontName=font_map['main'],
            fontSize=16,
            leading=20
        ),
        'center': ParagraphStyle(
            name='ThaiCenter',
            parent=styles['Normal'],
            fontName=font_map['main'],
            fontSize=16,
            alignment=TA_CENTER,
            leading=20
        ),
        'bold': ParagraphStyle(
            name='ThaiBold',
            parent=styles['Normal'],
            fontName=font_map['bold'],
            fontSize=16,
            leading=20
        ),
        'date': ParagraphStyle(
            name='ThaiDate',
            parent=styles['Normal'],
            fontName=font_map['main'],
            fontSize=16,
            leftIndent=9*cm,
            leading=20
        ),
        'title': ParagraphStyle(
            name='ThaiTitle',
            parent=styles['Normal'],
            fontName=font_map['bold'],
            fontSize=28,
            alignment=TA_CENTER,
            leading=32
        ),
        'company': ParagraphStyle(
            name='DadName',
            parent=styles['Normal'],
            fontName=font_map['title'],
            fontSize=28,
            alignment=TA_CENTER,
            leading=32,
            spaceAfter=5
        ),
        'address': ParagraphStyle(
            name='Address',
            parent=styles['Normal'],
            fontName=font_map['main'],
            fontSize=18,
            alignment=TA_CENTER,
            leading=20
        ),
        'tax': ParagraphStyle(
            name='TaxID',
            parent=styles['Normal'],
            fontName=font_map['main'],
            fontSize=16,
            alignment=TA_CENTER,
            leading=18
        )
    }
    
    return custom_styles


# ==========================================
# DATA FORMATTING
# ==========================================

def format_currency(amount):
    """Format number as Thai currency"""
    return f"{amount:,.2f}"


def get_thai_date():
    """Get current date in Thai format"""
    thai_months = [
        "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    now = datetime.now()
    thai_year = now.year + 543
    return f"วันที่ {now.day} {thai_months[now.month]} {thai_year}"


# ==========================================
# PDF GENERATION
# ==========================================

def create_pdf(quotation_data, output_filename="quotation.pdf"):
    """
    Create a professional quotation PDF
    
    Args:
        quotation_data (dict): Quotation information
        output_filename (str): Output PDF filename
        
    Returns:
        str: Output filename
    """
    # Setup fonts and styles
    font_map = register_thai_fonts()
    styles = create_styles(font_map)
    
    # Extract and format data
    total_price = quotation_data.get('total_price', 0)
    qty = quotation_data.get('quantity', 0)
    unit_price = quotation_data.get('unit_price', 0)
    
    # Format numbers
    str_qty = f"{qty:,}"
    str_unit_price = format_currency(unit_price)
    str_total = format_currency(total_price)
    thai_baht_text = bahttext(total_price)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    story = []
    
    # ==========================================
    # HEADER SECTION
    # ==========================================
    
    # Company information from environment variables
    story.append(Paragraph(COMPANY_NAME, styles['company']))
    story.append(Paragraph(COMPANY_ADDRESS, styles['address']))
    story.append(Paragraph(f"โทร. {COMPANY_PHONE}", styles['address']))
    story.append(Paragraph(
        f'เลขประจำตัวผู้เสียภาษีอากร <font size="12">{COMPANY_TAX_ID}</font>',
        styles['tax']
    ))
    story.append(Spacer(1, 0.5*cm))
    
    # Title
    story.append(Paragraph("ใบเสนอราคา", styles['title']))
    story.append(Spacer(1, 0.5*cm))
    
    # Date
    story.append(Paragraph(get_thai_date(), styles['date']))
    story.append(Spacer(1, 0.5*cm))
    
    # ==========================================
    # CUSTOMER SECTION
    # ==========================================
    
    customer_name = quotation_data.get('customer_name', '')
    customer_address = quotation_data.get('customer_address', '')
    
    story.append(Paragraph(f"<b>เรียน</b> {customer_name}", styles['normal']))
    
    if customer_address:
        # Add indented address
        story.append(Paragraph(
            f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{customer_address}",
            styles['normal']
        ))
    
    story.append(Paragraph("<b>เรื่อง</b> เสนอราคาจ้างเหมารถบัสพัดลม", styles['normal']))
    story.append(Spacer(1, 0.5*cm))
    
    # ==========================================
    # TABLE SECTION
    # ==========================================
    
    # Build destination details
    dest_name = quotation_data.get('destination', '')
    dest_address = quotation_data.get('destination_address', '')
    
    dest_full = dest_name
    if dest_address and dest_address not in dest_name:
        dest_full += f" {dest_address}"
    
    # Build item details
    project_name = quotation_data.get('project_name', '')
    date_start = quotation_data.get('date_start', '')
    date_end = quotation_data.get('date_end', '')
    item_desc = quotation_data.get('item_description', '')
    
    details = f"{project_name} {dest_full} ระหว่างวันที่ {date_start} - {date_end}"
    item_details = f"{item_desc}<br/>{details}"
    
    # Create table
    col_widths = [1.2*cm, 10.5*cm, 2.0*cm, 2.0*cm, 2.3*cm]
    
    table_data = [
        ['ลำดับที่', 'รายการ', 'จำนวนคัน', 'ราคา/คัน', 'จำนวนเงิน'],
        ['1', Paragraph(item_details, styles['normal']), str_qty, str_unit_price, str_total],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        [f'จำนวนเงินรวม ({thai_baht_text})', '', str_total, '', ''],
    ]
    
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_map['main']),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('VALIGN', (0, 1), (-1, -2), 'TOP'),
        ('ALIGN', (0, 1), (0, -2), 'CENTER'),
        ('ALIGN', (1, 1), (1, -2), 'LEFT'),
        ('ALIGN', (2, 1), (-1, -2), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -2), 0.5, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEAFTER', (0, 0), (-2, -2), 0.5, colors.black),
        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, -1), (1, -1)),
        ('ALIGN', (0, -1), (0, -1), 'CENTER'),
        ('SPAN', (2, -1), (4, -1)),
        ('ALIGN', (2, -1), (4, -1), 'RIGHT'),
        ('FONTNAME', (2, -1), (4, -1), font_map['bold']),
        ('GRID', (0, -1), (-1, -1), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 2.0, colors.black),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.2*cm))
    
    # ==========================================
    # FOOTER SECTION
    # ==========================================
    
    # Remark
    remark = quotation_data.get('remark', '')
    story.append(Paragraph(f"หมายเหตุ : {remark}", styles['bold']))
    story.append(Spacer(1, 2*cm))
    
    # Signature block
    quoter_fullname = f"{QUOTER_FIRSTNAME} {QUOTER_LASTNAME}"
    signature_data = [
        [Paragraph("ลงชื่อ ........................................................... ผู้เสนอราคา", styles['center'])],
        [Paragraph(f"({quoter_fullname})", styles['center'])],
        [Paragraph("ผู้เสนอราคา", styles['center'])]
    ]
    
    sig_table = Table(signature_data, colWidths=[10*cm])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    
    footer_table = Table([['', sig_table]], colWidths=[8*cm, 10*cm])
    story.append(footer_table)
    
    # Build PDF
    doc.build(story)
    
    return output_filename
    # Build PDF
    doc.build(story)
    
    return output_filename