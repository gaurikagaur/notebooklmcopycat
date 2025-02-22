import PyPDF2
import docx
import io

def extract_text(file_obj, extension):
    """
    Extract text from uploaded document based on file type
    """
    try:
        if extension == 'pdf':
            return extract_from_pdf(file_obj)
        elif extension == 'docx':
            return extract_from_docx(file_obj)
        elif extension == 'txt':
            return extract_from_txt(file_obj)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

def extract_from_pdf(file_obj):
    """
    Extract text from PDF files
    """
    text = ""
    pdf_reader = PyPDF2.PdfReader(file_obj)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.strip()

def extract_from_docx(file_obj):
    """
    Extract text from DOCX files
    """
    doc = docx.Document(file_obj)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text).strip()

def extract_from_txt(file_obj):
    """
    Extract text from TXT files
    """
    return file_obj.read().decode('utf-8').strip()
