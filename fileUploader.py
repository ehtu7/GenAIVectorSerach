import streamlit as st
from PyPDF2 import PdfReader
import db_reader_writer_service
from db_reader_writer_service import writeDataToDB
print(dir(db_reader_writer_service))

def read_pdf(file):
    """Extract text from a PDF file."""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def upload_File(inputFile):
    if inputFile:
    # Display file details
        st.write("### File Information")
        st.write(f"**File Name:** {inputFile.name}")
        st.write(f"**File Size:** {inputFile.size / 1024:.2f} KB")
    
        try:
        # Extract and display PDF content
            pdf_text = read_pdf(inputFile)
            writeDataToDB(pdf_text)
            st.write("### Extracted PDF Content:")
            st.text_area("PDF Content", pdf_text, height=300)
        except Exception as e:
            st.error(f"Error while reading the PDF file: {e}")
    else:
        st.info("Please upload a PDF file to view its content.")
