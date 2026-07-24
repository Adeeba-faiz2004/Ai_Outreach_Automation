
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(subject, email, lead):


    filename = f"{lead.name}_email.pdf"

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Outreach Email</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Name:</b> {lead.name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Company:</b> {lead.company}", styles["Normal"]))
    story.append(Paragraph(f"<b>Email:</b> {lead.email}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Subject:</b> {subject}", styles["Heading2"]))

    story.append(Paragraph(email.replace("\n", "<br/>"), styles["BodyText"]))

    pdf.build(story)

    return filename
