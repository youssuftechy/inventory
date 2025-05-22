from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.conf import settings
import tempfile

def generate_pdf(template_path, context):
    """Generate PDF file from HTML template."""
    # Render the HTML template
    html_string = render_to_string(template_path, context)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as output:
        # Generate PDF using WeasyPrint
        HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf(output)
        
    # Read the temporary file
    with open(output.name, 'rb') as f:
        pdf = f.read()
        
    return pdf

def generate_pdf_response(pdf_content, filename):
    """Create HTTP response with PDF content."""
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
