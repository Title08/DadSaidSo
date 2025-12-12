from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bahttext import bahttext
from datetime import datetime
import os

# --- Fonts Setup ---
def get_font_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fonts', filename)

def register_fonts_robust():
    f_regular = get_font_path('THSarabunNew.ttf')
    f_bold = get_font_path('THSarabunNew Bold.ttf')
    f_italic = get_font_path('THSarabunNew Italic.ttf')
    f_bold_italic = get_font_path('THSarabunNew BoldItalic.ttf')

    font_cfg = {'main': 'Helvetica', 'bold': 'Helvetica-Bold', 'title': 'Helvetica-Bold'}

    if os.path.exists(f_regular):
        pdfmetrics.registerFont(TTFont('THSarabunNew', f_regular))
        font_cfg['main'] = 'THSarabunNew'
    elif os.path.exists('THSarabunNew.ttf'): # Try local dir
         pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))
         font_cfg['main'] = 'THSarabunNew'
    
    if font_cfg['main'] == 'Helvetica': return font_cfg

    has_bold = False
    if os.path.exists(f_bold):
        pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', f_bold))
        font_cfg['bold'] = 'THSarabunNew-Bold'
        has_bold = True
    else:
        from reportlab.lib.fonts import addMapping
        addMapping('THSarabunNew', 1, 0, 'THSarabunNew')
        font_cfg['bold'] = 'THSarabunNew'

    if os.path.exists(f_bold_italic):
        pdfmetrics.registerFont(TTFont('THSarabunNew-BoldItalic', f_bold_italic))
        font_cfg['title'] = 'THSarabunNew-BoldItalic'
    elif has_bold:
        font_cfg['title'] = 'THSarabunNew-Bold'
    else:
        font_cfg['title'] = 'THSarabunNew'
        
    if os.path.exists(f_italic):
        pdfmetrics.registerFont(TTFont('THSarabunNew-Italic', f_italic))

    return font_cfg

def create_pdf(quotation_data, output_filename="quotation.pdf"):
    font_map = register_fonts_robust()
    font_name = font_map['main']
    bold_font = font_map['bold']
    title_font = font_map['title']
    
    # Data Prep
    total_price = quotation_data.get('total_price', 0)
    qty = quotation_data.get('quantity', 0)
    u_price = quotation_data.get('unit_price', 0)
    str_qty = "{:,}".format(qty)
    str_u_price = "{:,.2f}".format(u_price)
    str_total = "{:,.2f}".format(total_price)
    thai_text = bahttext(total_price)

    doc = SimpleDocTemplate(output_filename, pagesize=A4,
                            rightMargin=1.5*cm, leftMargin=1.5*cm, 
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    story = []
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle(name='ThaiNormal', parent=styles['Normal'], fontName=font_name, fontSize=16, leading=20)
    style_center = ParagraphStyle(name='ThaiCenter', parent=styles['Normal'], fontName=font_name, fontSize=16, alignment=TA_CENTER, leading=20)
    style_bold_text = ParagraphStyle(name='ThaiBold', parent=styles['Normal'], fontName=bold_font, fontSize=16, leading=20)
    style_date = ParagraphStyle(name='ThaiDate', parent=styles['Normal'], fontName=font_name, fontSize=16, alignment=TA_LEFT, leftIndent=9*cm, leading=20)
    style_title = ParagraphStyle(name='ThaiTitle', parent=styles['Normal'], fontName=bold_font, fontSize=28, alignment=TA_CENTER, leading=32)
    style_dad_name = ParagraphStyle(name='DadName', parent=styles['Normal'], fontName=title_font, fontSize=28, alignment=TA_CENTER, leading=32, spaceAfter=5)
    style_address = ParagraphStyle(name='Address', parent=styles['Normal'], fontName=font_name, fontSize=18, alignment=TA_CENTER, leading=20)
    style_tax_id = ParagraphStyle(name='TaxID', parent=styles['Normal'], fontName=font_name, fontSize=16, alignment=TA_CENTER, leading=18)

    # --- Header ---
    # Mock Data for GitHub Version
    story.append(Paragraph("ชื่อบริษัท/ร้านค้า ของคุณ", style_dad_name)) 
    story.append(Paragraph("ที่อยู่ของคุณ ต.ตำบล อ.อำเภอ จ.จังหวัด 00000", style_address)) 
    story.append(Paragraph("โทร. 08x-xxxxxxx", style_address))
    story.append(Paragraph('เลขประจำตัวผู้เสียภาษีอากร <font size="12">0000000000000</font>', style_tax_id))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("ใบเสนอราคา", style_title))
    story.append(Spacer(1, 0.5*cm))

    # Date
    months = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    now = datetime.now()
    thai_date = f"วันที่ {now.day} {months[now.month]} {now.year + 543}"
    story.append(Paragraph(thai_date, style_date))
    story.append(Spacer(1, 0.5*cm))

    # --- Customer Section (Updated with Address) ---
    cust_name = quotation_data.get('customer_name', '')
    cust_addr = quotation_data.get('customer_address', '') # รับที่อยู่ลูกค้าจาก AI
    
    story.append(Paragraph(f"<b>เรียน</b> {cust_name}", style_normal))
    
    # ถ้ามีที่อยู่ ให้แสดงบรรทัดถัดมาพร้อมย่อหน้า
    if cust_addr:
        # ใช้ &nbsp; เพื่อเว้นวรรคย่อหน้า
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{cust_addr}", style_normal))
        
    story.append(Paragraph(f"<b>เรื่อง</b> เสนอราคาจ้างเหมารถบัสพัดลม", style_normal))
    story.append(Spacer(1, 0.5*cm))

    # --- Table ---
    col_widths = [1.2*cm, 10.5*cm, 2.0*cm, 2.0*cm, 2.3*cm]
    
    # รวมรายละเอียด: ชื่อโครงการ + สถานที่ + ที่อยู่สถานที่ + วันที่
    dest_name = quotation_data.get('destination', '')
    dest_addr = quotation_data.get('destination_address', '') # รับที่อยู่สถานที่จาก AI
    
    # Logic การต่อข้อความ
    dest_full = dest_name
    if dest_addr and dest_addr not in dest_name: # กันข้อมูลซ้ำ
        dest_full += f" {dest_addr}"

    details_flow = f"{quotation_data.get('project_name','')} {dest_full} ระหว่างวันที่ {quotation_data.get('date_start','')} - {quotation_data.get('date_end','')}"
    
    item_details = f"{quotation_data.get('item_description','')}<br/>{details_flow}"
    
    data = [
        ['ลำดับที่', 'รายการ', 'จำนวนคัน', 'ราคา/คัน', 'จำนวนเงิน'], 
        ['1', Paragraph(item_details, style_normal), str_qty, str_u_price, str_total], 
        ['', '', '', '', ''], 
        ['', '', '', '', ''], 
        [f'จำนวนเงินรวม ({thai_text})', '', str_total, '', ''], 
    ]

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), font_name),
        ('FONTSIZE', (0,0), (-1,-1), 16),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
        ('VALIGN', (0,1), (-1,-2), 'TOP'),
        ('ALIGN', (0,1), (0,-2), 'CENTER'),
        ('ALIGN', (1,1), (1,-2), 'LEFT'),
        ('ALIGN', (2,1), (-1,-2), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-2), 0.5, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEAFTER', (0,0), (-2,-2), 0.5, colors.black),
        ('VALIGN', (0,-1), (-1,-1), 'MIDDLE'),
        ('SPAN', (0,-1), (1,-1)),
        ('ALIGN', (0,-1), (0,-1), 'CENTER'),
        ('SPAN', (2,-1), (4,-1)),
        ('ALIGN', (2,-1), (4,-1), 'RIGHT'),
        ('FONTNAME', (2,-1), (4,-1), bold_font),
        ('GRID', (0,-1), (-1,-1), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 2.0, colors.black),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 0.2*cm))
    
    # Remark
    story.append(Paragraph(f"หมายเหตุ : {quotation_data.get('remark','')}", style_bold_text))
    story.append(Spacer(1, 2*cm))

    # Signature
    signature_block = [
        [Paragraph(f"ลงชื่อ ........................................................... ผู้เสนอราคา", style_center)],
        [Paragraph(f"(ชื่อ-นามสกุล ผู้เสนอราคา)", style_center)],
        [Paragraph(f"ผู้เสนอราคา", style_center)]
    ]
    sig_table = Table(signature_block, colWidths=[10*cm])
    sig_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer_table = Table([['', sig_table]], colWidths=[8*cm, 10*cm])
    story.append(footer_table)

    doc.build(story)
    return output_filename