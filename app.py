import streamlit as st
import re
from genkou_yooshi_generator_2 import generate_pdf_from_string
import base64

# Set up the Streamlit app
st.set_page_config(
    page_title="Japanese Handwriting Practice",  # This will show in browser tab
    page_icon="🍙",  # Can be an emoji or image path
    layout="centered",  # Optional: "centered" or "wide"
)
st.title("🍙 Japanese Handwriting Practice PDF Generator")
st.write("This app generates a genkō yōshi PDF for handwriting practice based on Japanese sentences you provide.")

# Function to check if text contains Japanese characters
def contains_japanese(text):
    """Return True if text contains Japanese characters."""
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text))

# Function to check character limit
def check_char_limits(content, max_chars=2000, max_words=300):
    """Check if content exceeds limits"""
    char_count = len(content)
    #word_count = len(content.split())
    
    return {
        'char_count': char_count,
        #'word_count': word_count,
            'char_limit_exceeded': char_count > max_chars,
            #'word_limit_exceeded': word_count > max_words,
            'within_limits': char_count <= max_chars  # and word_count <= max_words
        }


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

def show_pdf_viewer(pdf_data):
    """Show PDF using PDF.js viewer"""
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    
    # PDF.js viewer
    pdf_display = f"""
    <div style="width:100%; height:600px;">
        <object data="data:application/pdf;base64,{base64_pdf}" 
                type="application/pdf" 
                width="100%" 
                height="600px">
            <p>Your browser doesn't support PDF viewing. 
               <a href="data:application/pdf;base64,{base64_pdf}" download="handwriting_practice.pdf">
                   Download the PDF
               </a>
            </p>
        </object>
    </div>
    """
    
    st.markdown(pdf_display, unsafe_allow_html=True)
        

# Set char limit
MAX_CHARS =  2000  # Adjust as needed
# Create input for sentences
sentences = st.text_area(
    "Enter Japanese sentences:", 
    height=200, 
    placeholder="Paste or type your text here...",
    max_chars=MAX_CHARS,
    help=f"Maximum {MAX_CHARS} characters"
)


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
            # Show preview
            show_pdf_viewer(pdf_data)
