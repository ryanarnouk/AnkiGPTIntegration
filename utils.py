from pypdf import PdfReader
import json

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    page = reader.pages[0]
    text = page.extract_text()
    return text

def parse_json(str):
    return json.loads(str)