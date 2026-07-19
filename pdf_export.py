import markdown
from xhtml2pdf import pisa

def convert_md_to_pdf(md_text: str, output_path: str):
    html = markdown.markdown(md_text, extensions=["extra"])
    styled_html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.5; }}
        h1 {{ font-size: 20pt; }}
        h2 {{ font-size: 15pt; margin-top: 20px; }}
        ul {{ margin-left: 15px; }}
    </style>
    </head>
    <body>{html}</body>
    </html>
    """
    with open(output_path, "wb") as f:
        result = pisa.CreatePDF(styled_html, dest=f)
    return result.err  # 0 means success