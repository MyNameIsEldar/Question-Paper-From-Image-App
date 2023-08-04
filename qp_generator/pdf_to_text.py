import PyPDF2
import streamlit as st

@st.cache_data
def main(uploaded_file, pages):
    
    pdf_text = []
    pdf_file = PyPDF2.PdfFileReader(uploaded_file)
    
    for page in pages:
        pdf_page = pdf_file.getPage(page) 
        page_text = pdf_page.extractText()
        pdf_text.append(page_text)
    
    pdf_text = '\n'.join(pdf_text)
    return pdf_text