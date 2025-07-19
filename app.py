import streamlit as st
import base64
import re
from genkou_yooshi_generator_2 import generate_pdf_from_string

st.title("🍙 Japanese Handwriting Practice PDF Generator")
st.write("This app generates a genkō yōshi PDF for handwriting practice based on Japanese sentences you provide.")

# Create input for sentences
sentences = st.text_area("Enter Japanese sentences:", height=200, placeholder="Paste or type your text here...")

# Function to check if text contains Japanese characters
def contains_japanese(text):
    """Return True if text contains Japanese characters."""
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text))

# Function to generate PDF and display it with print dialog
def display_pdf_with_print(pdf_data, filename="handwriting_practice.pdf"):
    """Most reliable cross-browser approach"""
    col1, col2, col3 = st.columns([1,2,1])
    with col2:        
        # Big, prominent download button
        st.download_button(
            label="📄 Download Your PDF",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
        
        # Simple instructions
        st.info("The PDF will download to your device and should open automatically in your browser or PDF reader.")


# Button to generate PDF
if st.button("Generate PDF", type="primary"):
    if not sentences:
        st.error("Please enter at least one sentence.")
    elif not contains_japanese(sentences):
        st.error("No Japanese input detected. Please enter Japanese text.")
    else:
        with st.spinner("Generating PDF..."):
            pdf_data = generate_pdf_from_string(sentences)
            st.success(f"🎉 Your PDF is ready!")
            display_pdf_with_print(pdf_data)

