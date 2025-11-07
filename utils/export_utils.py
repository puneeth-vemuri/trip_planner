from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
import re


def generate_pdf_from_text(text: str, title: str = "Trip Plan") -> bytes:
    """Generate a PDF from markdown-formatted text with proper styling."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER, 
                           leftMargin=1*inch, rightMargin=1*inch,
                           topMargin=1*inch, bottomMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1a1a1a',
        spaceAfter=20,
        alignment=TA_LEFT
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c3e50',
        spaceAfter=12,
        spaceBefore=12,
        alignment=TA_LEFT
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='#34495e',
        spaceAfter=10,
        spaceBefore=10,
        alignment=TA_LEFT
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#333333',
        spaceAfter=8,
        alignment=TA_LEFT,
        leading=14
    )
    
    # Build document
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Process text line by line
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Convert markdown to HTML for ReportLab
        # Handle headers (## or ###)
        if line.startswith('### '):
            clean_line = line[4:].strip()
            story.append(Paragraph(clean_line, subheading_style))
        elif line.startswith('## '):
            clean_line = line[3:].strip()
            story.append(Paragraph(clean_line, heading_style))
        elif line.startswith('# '):
            clean_line = line[2:].strip()
            story.append(Paragraph(clean_line, heading_style))
        else:
            # Convert markdown bold (**text**) to HTML bold (<b>text</b>)
            html_line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            
            # Convert markdown italic (*text*) to HTML italic (<i>text</i>)
            html_line = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', html_line)
            
            # Handle bullet points
            if html_line.startswith('- ') or html_line.startswith('• '):
                html_line = '• ' + html_line[2:]
            
            # Escape special characters but keep our HTML tags
            # (ReportLab's Paragraph handles basic HTML)
            
            story.append(Paragraph(html_line, body_style))
    
    # Build PDF
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
