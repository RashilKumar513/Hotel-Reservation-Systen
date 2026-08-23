import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_invoice(bill_no, customer, phone, order_type, table_no, payment, notes,
                         rows, subtotal, discount, tax_pct, tax_amount, grand_total):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#4c1d95'),
        alignment=1 # Center
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#6b7280'),
        alignment=1 # Center
    )
    
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1f2937')
    )
    
    normal_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#374151')
    )

    bold_style = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#111827')
    )

    right_bold = ParagraphStyle(
        'RightBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        alignment=2, # Right
        textColor=colors.HexColor('#111827')
    )
    
    right_normal = ParagraphStyle(
        'RightNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        alignment=2,
        textColor=colors.HexColor('#374151')
    )

    elements = []
    
    # 1. Header
    elements.append(Paragraph("5 STAR RESTAURANT", title_style))
    elements.append(Paragraph("123 Gourmet Avenue, Food City • Tel: +91 98765 43210", subtitle_style))
    elements.append(Paragraph("TAX INVOICE / RECEIPT", ParagraphStyle('SubHeader', parent=subtitle_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#d97706'), fontSize=11, leading=15)))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#4c1d95'), spaceAfter=15))

    # 2. Metadata Grid (Bill info & Customer info)
    now_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    meta_data = [
        [
            Paragraph(f"<b>Bill No:</b> {bill_no}", normal_style),
            Paragraph(f"<b>Customer:</b> {customer or 'Guest'}", normal_style)
        ],
        [
            Paragraph(f"<b>Date & Time:</b> {now_str}", normal_style),
            Paragraph(f"<b>Phone:</b> {phone or '-'}", normal_style)
        ],
        [
            Paragraph(f"<b>Order Type:</b> {order_type}", normal_style),
            Paragraph(f"<b>Table No:</b> {table_no or '-'}", normal_style)
        ],
        [
            Paragraph(f"<b>Payment Mode:</b> {payment}", normal_style),
            Paragraph(f"<b>Notes:</b> {notes or '-'}", normal_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[260, 260])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#f3f4f6')),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 15))

    # 3. Itemized Table
    table_data = [[
        Paragraph("<b>S.No</b>", bold_style),
        Paragraph("<b>Category</b>", bold_style),
        Paragraph("<b>Item Description</b>", bold_style),
        Paragraph("<b>Qty</b>", bold_style),
        Paragraph("<b>Unit Price (₹)</b>", right_bold),
        Paragraph("<b>Amount (₹)</b>", right_bold)
    ]]

    for i, r in enumerate(rows, 1):
        cat = r.get("Category") or r.get("category", "")
        item_name = r.get("Item") or r.get("item", "")
        qty = r.get("Qty") if "Qty" in r else r.get("qty", 0)
        unit_price = float(r.get("Unit Price") if "Unit Price" in r else r.get("unit_price", 0.0))
        amount = float(r.get("Amount") if "Amount" in r else r.get("amount", 0.0))

        table_data.append([
            Paragraph(str(i), normal_style),
            Paragraph(str(cat), normal_style),
            Paragraph(str(item_name), bold_style),
            Paragraph(str(qty), normal_style),
            Paragraph(f"{unit_price:.2f}", right_normal),
            Paragraph(f"{amount:.2f}", right_bold)
        ])

    item_table = Table(table_data, colWidths=[35, 100, 185, 40, 80, 80])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4c1d95')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fcfaff')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e9d5ff')),
    ]))
    
    # Fix header row text color inside Paragraphs
    table_data[0] = [
        Paragraph("<b>S.No</b>", ParagraphStyle('W', parent=bold_style, textColor=colors.white)),
        Paragraph("<b>Category</b>", ParagraphStyle('W', parent=bold_style, textColor=colors.white)),
        Paragraph("<b>Item Description</b>", ParagraphStyle('W', parent=bold_style, textColor=colors.white)),
        Paragraph("<b>Qty</b>", ParagraphStyle('W', parent=bold_style, textColor=colors.white)),
        Paragraph("<b>Unit Price</b>", ParagraphStyle('WR', parent=right_bold, textColor=colors.white)),
        Paragraph("<b>Amount</b>", ParagraphStyle('WR', parent=right_bold, textColor=colors.white))
    ]
    item_table = Table(table_data, colWidths=[35, 100, 185, 40, 80, 80])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4c1d95')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fcfaff')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e9d5ff')),
    ]))

    elements.append(item_table)
    elements.append(Spacer(1, 10))

    # 4. Summary & Tax Table
    cgst_rate = tax_pct / 2.0
    sgst_rate = tax_pct / 2.0
    cgst_amount = tax_amount / 2.0
    sgst_amount = tax_amount / 2.0

    summary_data = [
        [Paragraph("Subtotal:", normal_style), Paragraph(f"₹ {subtotal:,.2f}", right_normal)],
        [Paragraph("Discount:", normal_style), Paragraph(f"- ₹ {discount:,.2f}", right_normal)],
        [Paragraph(f"CGST ({cgst_rate:.1f}%):", normal_style), Paragraph(f"₹ {cgst_amount:,.2f}", right_normal)],
        [Paragraph(f"SGST ({sgst_rate:.1f}%):", normal_style), Paragraph(f"₹ {sgst_amount:,.2f}", right_normal)],
        [
            Paragraph("<b>GRAND TOTAL:</b>", ParagraphStyle('GT', parent=bold_style, fontSize=11, textColor=colors.HexColor('#4c1d95'))),
            Paragraph(f"<b>₹ {grand_total:,.2f}</b>", ParagraphStyle('GTR', parent=right_bold, fontSize=11, textColor=colors.HexColor('#4c1d95')))
        ]
    ]

    summary_table = Table(summary_data, colWidths=[140, 100])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.HexColor('#4c1d95')),
        ('LINEABOVE', (0,-1), (-1,-1), 1, colors.HexColor('#4c1d95')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f3e8ff')),
    ]))

    # Wrap summary table in outer table for alignment to right
    wrapper_table = Table([["", summary_table]], colWidths=[280, 240])
    wrapper_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))

    elements.append(wrapper_table)
    elements.append(Spacer(1, 20))

    # 5. Footer & Terms
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#d1d5db'), spaceAfter=10))
    footer_text = Paragraph(
        "Thank you for dining with 5 Star Restaurant! ❤️<br/>"
        "<i>This is a computer generated tax invoice. No signature required.</i>",
        subtitle_style
    )
    elements.append(footer_text)

    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
