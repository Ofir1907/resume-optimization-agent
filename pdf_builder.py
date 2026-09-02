import io
import re
import unicodedata
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from schemas import TailoredResume


PRIMARY_ACCENT_COLOR = colors.HexColor("#F372AE")
# ==============================================================================
# 2. PDF Generator (1:1 Match with Original CV Format)
# ==============================================================================
def sanitize_text(text: str) -> str:
    """Sanitizes text by replacing problematic Unicode glyphs with ASCII/HTML equivalents."""
    if not text:
        return ""
    
    # 1. Normalize Unicode representation (NFKC turns compatibility characters into standard forms)
    text = unicodedata.normalize('NFKC', str(text))
    
    # 2. Catch all Unicode hyphen, dash, and minus variations and replace with standard ASCII hyphen (-)
    # Covers: soft hyphen (\xad), non-breaking hyphen (\u2011), en-dash (\u2013), em-dash (\u2014),
    # figure dash (\u2012), horizontal bar (\u2015), minus sign (\u2212), etc.
    hyphen_pattern = r'[\u00ad\u2010\u2011\u2012\u2013\u2014\u2015\u2212\ufe58\ufe63\uff0d]'
    text = re.sub(hyphen_pattern, '-', text)

    text = text.replace('\u00a0', ' ')
    # 3. Replace fancy quotation marks and apostrophes
    text = re.sub(r'[\u2018\u2019\u201a\u201b]', "'", text)
    text = re.sub(r'[\u201c\u201d\u201e\u201f]', '"', text)
    
    # 4. Replace bullet characters with HTML entity
    text = re.sub(r'[\u2022\u2023\u25e6\u2043\u2219]', '&bull;', text)
    
    # 5. Remove any remaining non-printable / control characters (except standard newlines/tabs)
    text = "".join(ch for ch in text if ch == '\n' or ch == '\t' or unicodedata.category(ch)[0] != 'C')
    
    return text

import io
import re
import unicodedata
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def sanitize_text(text: str) -> str:
    """Bulletproof sanitization to guarantee ZERO black boxes in ReportLab Helvetica."""
    if not text:
        return ""
    
    text = str(text)

    #General Unicode Normalization (NFKC) to standardize characters
    text = "".join('-' if unicodedata.category(ch) == 'Pd' else ch for ch in text)

    #Normalize hyphens/dashes to standard ASCII hyphen
    text = re.sub(r'[\u00ad\u2212\ufe58\ufe63\uff0d]', '-', text)

    # Replace non-breaking spaces and other whitespace variations with standard space
    text = re.sub(r'[\u00a0\u2000-\u200b\u202f\u205f\u3000]', ' ', text)

    # Replace fancy quotes and apostrophes with standard ASCII equivalents
    text = re.sub(r'[\u2018\u2019\u201a\u201b`]', "'", text)
    text = re.sub(r'[\u201c\u201d\u201e\u201f«»]', '"', text)

    # Replace bullet characters with HTML entity to avoid black boxes
    text = re.sub(r'[\u2022\u2023\u25e6\u2043\u2219\u25aa\u25ab]', '&bull;', text)

    # Remove any remaining non-printable/control characters (except standard newlines/tabs)
    cleaned_chars = []
    for ch in text:
        # Keep standard ASCII characters, letters from other languages, and replace others with space
        if ord(ch) < 128:
            cleaned_chars.append(ch)
        elif unicodedata.category(ch).startswith('L'):  
            cleaned_chars.append(ch)
        else:
            cleaned_chars.append(' ')

    return "".join(cleaned_chars)

def create_pdf_cv(data: TailoredResume) -> io.BytesIO:
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=28,
        bottomMargin=28
    )

    PRIMARY_ACCENT_COLOR = colors.HexColor("#F372AE")
    TEXT_DARK = colors.HexColor('#1F2937')

    styles = getSampleStyleSheet()

    header_title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        alignment=1,
        textColor=PRIMARY_ACCENT_COLOR
    )

    contact_style = ParagraphStyle(
        'ContactHeader',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        alignment=1,
        textColor=TEXT_DARK
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=PRIMARY_ACCENT_COLOR,
        spaceBefore=4,
        spaceAfter=1.5
    )

    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK,
        spaceBefore=2,
        spaceAfter=1
    )

    # 2. Increased body font size & comfortable line height
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=11,
        bulletIndent=2,
        spaceAfter=1
    )
    story = []

    def add_section_header(title: str):
        story.append(Paragraph(title, section_heading))
        story.append(HRFlowable(
            width="100%",
            thickness=0.5,
            color=PRIMARY_ACCENT_COLOR,
            spaceAfter=2,
            spaceBefore=0.5
        ))

    # 1. Header (Centered Name, Title & Contact)
    header_text = sanitize_text(f"{data.personal_info.name} - {data.personal_info.title}")
    story.append(Paragraph(header_text, header_title_style))
    story.append(Spacer(1, 1.5))

    c = data.personal_info.contact
    line1_parts = [
        f"<b>Phone:</b> {c.phone}" if c.phone else "",
        f"<b>LinkedIn:</b> {c.linkedin}" if c.linkedin else ""
    ]
    line1 = " &nbsp;|&nbsp; ".join([p for p in line1_parts if p])

    line2_parts = [
        f"<b>E-mail:</b> {c.email}" if c.email else "",
        f"<b>GitHub:</b> {c.github}" if c.github else ""
    ]
    line2 = " &nbsp;|&nbsp; ".join([p for p in line2_parts if p])

    if line1:
        story.append(Paragraph(sanitize_text(line1), contact_style))
    if line2:
        story.append(Paragraph(sanitize_text(line2), contact_style))

    story.append(Spacer(1, 1.5))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=2.5))

    # 2. ABOUT ME
    add_section_header("ABOUT ME")
    story.append(Paragraph(sanitize_text(data.about_me), body_style))
    story.append(Spacer(1, 1.5))

    # 3. WORK EXPERIENCE
    add_section_header("WORK EXPERIENCE")
    for job in data.work_experience:
        header = sanitize_text(f"<b>{job.role}, {job.organization}</b> ({job.period})")
        story.append(Paragraph(header, body_style))
        for bullet in job.highlights:
            story.append(Paragraph(f"&bull; {sanitize_text(bullet)}", bullet_style))
        story.append(Spacer(1, 1))

    # Technical Projects
    if data.technical_projects:
        add_section_header("TECHNICAL PROJECTS")
        for proj in data.technical_projects:
            proj_header = sanitize_text(f"<b>{proj.name}</b> | <i>{proj.technologies}</i>")
            story.append(Paragraph(proj_header, body_style))
            for bullet in proj.highlights:
                story.append(Paragraph(f"&bull; {sanitize_text(bullet)}", bullet_style))
            story.append(Spacer(1, 1))

    # 4. PROFESSIONAL SKILLS
    add_section_header("PROFESSIONAL SKILLS")
    s = data.professional_skills
    skills_map = [
        ("Languages", s.languages),
        ("Software Development", s.software_development),
        ("Data Analysis & Visualization", s.data_analysis_and_visualization),
        ("Environments", s.environments),
        ("Bioinformatics Tools", s.bioinformatics_and_domain_tools),
        ("Machine Learning", s.machine_learning),
        ("Soft Skills", s.soft_skills),
    ]
    for label, items in skills_map:
        if items:
            clean_items = [sanitize_text(it) for it in items]
            skill_line = f"<b>{label}:</b> {', '.join(clean_items)}."
            story.append(Paragraph(skill_line, body_style))
            story.append(Spacer(1, 0.3))
    story.append(Spacer(1, 1))

    # 5. EDUCATION
    add_section_header("EDUCATION")
    for edu in data.education:
        edu_line = f"<b>{edu.degree}</b>, {edu.institution} ({edu.period})"
        if edu.honors_or_notes:
            edu_line += f", {edu.honors_or_notes}"
        story.append(Paragraph(sanitize_text(edu_line), body_style))
        story.append(Spacer(1, 0.3))
    story.append(Spacer(1, 1))

    # 6. MILITARY SERVICE
    if data.military_service:
        mil = data.military_service[0] if isinstance(data.military_service, list) and data.military_service else data.military_service
        if getattr(mil, 'role', None):
            add_section_header("MILITARY SERVICE")
            story.append(Paragraph(sanitize_text(f"<b>{mil.role}</b> ({mil.period})"), body_style))
            story.append(Paragraph(sanitize_text(mil.description), body_style))
            story.append(Spacer(1, 1))

    # 7. LANGUAGES
    if data.languages:
        add_section_header("LANGUAGES")
        lang_parts = [sanitize_text(f"<b>{lang.language}:</b> {lang.proficiency}") for lang in data.languages]
        story.append(Paragraph(" &nbsp;|&nbsp; ".join(lang_parts), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer