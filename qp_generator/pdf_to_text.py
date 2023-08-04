import PyPDF2
import streamlit as st

@st.cache_data
def main(uploaded_file, pages):
    
    pages = range(pages[0]-1, pages[-1])
    pdf_text = []
    pdf_file = PyPDF2.PdfReader(uploaded_file)
    
    for page in pages:
        pdf_page = pdf_file.pages[page]
        page_text = pdf_page.extract_text()
        pdf_text.append(page_text)
    
    pdf_text = ' '.join(pdf_text)
    return pdf_text


@st.cache_data
def pages_count(uploaded_file):
    pdf_file = PyPDF2.PdfReader(uploaded_file)

    return len(pdf_file.pages)