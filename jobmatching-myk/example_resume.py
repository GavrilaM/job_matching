"""Script to generate a sample resume PDF for testing."""
from fpdf import FPDF

def create_sample_resume():
    """Create a sample resume PDF using built-in fonts."""
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 10, "John Developer", ln=True, align='C')
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, "john.developer@email.com | (555) 123-4567", ln=True, align='C')
    pdf.cell(0, 10, "123 Tech Street, Silicon Valley, CA 94025", ln=True, align='C')

    # Summary
    pdf.ln(10)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "Professional Summary", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, "Experienced software developer with 5 years of expertise in full-stack development, specializing in Python and JavaScript frameworks.")

    # Experience
    pdf.ln(5)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "Work Experience", ln=True)

    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 10, "Senior Software Developer - Tech Corp (2020-Present)", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, "- Led development of microservices architecture\n- Implemented CI/CD pipelines\n- Managed team of 5 developers")

    pdf.ln(5)
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 10, "Software Developer - StartUp Inc. (2018-2020)", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, "- Developed RESTful APIs using Flask\n- Implemented React-based front-end\n- Optimized database queries")

    # Education
    pdf.ln(5)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, "Master of Science in Computer Science\nStanford University (2016-2018)\n\nBachelor of Science in Software Engineering\nMIT (2012-2016)")

    # Skills
    pdf.ln(5)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "Technical Skills", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, "Programming: Python, JavaScript, Java, C++\nFrameworks: React, Flask, Django, Node.js\nTools: Docker, Kubernetes, Git\nDatabases: PostgreSQL, MongoDB")

    pdf.ln(5)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, "Soft Skills", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, "- Leadership\n- Problem Solving\n- Team Management\n- Communication")

    # Save the PDF
    output_path = "sample_resume.pdf"
    pdf.output(output_path)
    print(f"Sample resume created: {output_path}")

if __name__ == "__main__":
    create_sample_resume()