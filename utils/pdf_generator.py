
import os
from xml.sax.saxutils import escape

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(subject, email, lead):

    os.makedirs("exports", exist_ok=True)

    # Include the email address so two leads with the same name never
    # overwrite each other's PDF file.
    safe_name = lead.name.replace(" ", "_")
    safe_email = lead.email.replace("@", "_at_").replace(".", "_")
    filename = os.path.join("exports", f"{safe_name}_{safe_email}.pdf")

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Outreach Email</b>", styles["Title"]))

    # Escape user/AI generated content so stray characters like & < >
    # don't break ReportLab's mini-XML parser and crash PDF generation.
    story.append(Paragraph(f"<b>Name:</b> {escape(lead.name)}", styles["Normal"]))
    story.append(Paragraph(f"<b>Company:</b> {escape(lead.company)}", styles["Normal"]))
    story.append(Paragraph(f"<b>Email:</b> {escape(lead.email)}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Subject:</b> {escape(subject)}", styles["Heading2"]))

    story.append(Paragraph(escape(email).replace("\n", "<br/>"), styles["BodyText"]))

    pdf.build(story)

    return filename
