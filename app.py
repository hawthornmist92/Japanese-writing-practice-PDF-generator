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
def display_pdf_with_print(pdf_data):
    """Display PDF and automatically open print dialog"""
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    
    pdf_display = f'''
    <iframe src="data:application/pdf;base64,{base64_pdf}" 
            width="700" height="1000" type="application/pdf"
            id="pdf-frame"></iframe>
    <script>
        // Wait for PDF to load, then trigger print
        setTimeout(function() {{
            window.print();
        }}, 1000);
    </script>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)

# Button to generate PDF
if st.button("Generate PDF"):
    if not sentences:
        st.error("Please enter at least one sentence.")
    elif not contains_japanese(sentences):
        st.error("No Japanese input detected. Please enter Japanese text.")
    else:
        pdf_data = generate_pdf_from_string(sentences)
        st.success(f"PDF generated successfully!")
        display_pdf_with_print(pdf_data)

