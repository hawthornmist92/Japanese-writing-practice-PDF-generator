import streamlit as st
import re
from genkou_yooshi_generator_2 import generate_pdf_from_string
import base64
from streamlit_pdf_viewer import pdf_viewer

# Set up the Streamlit app
st.set_page_config(
    page_title="Japanese Handwriting Practice",  # This will show in browser tab
    page_icon="🍙",  # Can be an emoji or image path
    layout="wide",  # Optional: "centered" or "wide"
)

# Title of the app
st.title("🍙 Japanese Handwriting Practice PDF Generator")

# Use columns for layout
left_col, right_col = st.columns([1, 1.5])

# State variables
if 'pdf_data' not in st.session_state:
    st.session_state['pdf_data'] = None

with left_col:
    st.write("This app generates a genkō yōshi PDF for handwriting practice based on Japanese sentences you provide.")

    # Function to check if text contains Japanese characters
    def contains_japanese(text):
        """Return True if text contains Japanese characters."""
        return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text))

    # Function to check character limit
    def check_char_limits(content, max_chars=2000, max_words=300):
        """Check if content exceeds limits"""
        char_count = len(content)
        return {
            'char_count': char_count,
            'char_limit_exceeded': char_count > max_chars,
            'within_limits': char_count <= max_chars
        }

    # Set char limit
    MAX_CHARS = 2000
    # Create input for sentences
    sentences = st.text_area(
        "Enter Japanese sentences:",
        height=200,
        placeholder="Paste or type your text here...",
        max_chars=MAX_CHARS,
        help=f"Maximum {MAX_CHARS} characters"
    )
    generate = st.button("Generate PDF", type="primary")

    # Handle button logic and messages
    if generate:
        if not sentences:
            st.error("Please enter at least one sentence.")
            st.session_state['pdf_data'] = None
        elif not contains_japanese(sentences):
            st.error("No Japanese input detected. Please enter Japanese text.")
            st.session_state['pdf_data'] = None
        else:
            with st.spinner("Generating PDF..."):
                pdf_data = generate_pdf_from_string(sentences)
                st.session_state['pdf_data'] = pdf_data
                st.success("🎉 Your PDF is ready!")
    # Show download button if PDF is ready
    if st.session_state.get('pdf_data'):
        st.download_button(
            label="📄 Download Your PDF",
            data=st.session_state['pdf_data'],
            file_name="handwriting_practice.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )

with right_col:
    # Only show PDF preview if PDF is ready
    if st.session_state.get('pdf_data'):
        pdf_viewer(st.session_state['pdf_data'])



