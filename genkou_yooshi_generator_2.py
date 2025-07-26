#!/usr/bin/env python3
# """
# Genkō Yōshi Handwriting Practice Worksheet Generator
# Converts Japanese sentences from text files into handwriting practice worksheets.
# """

import re
import argparse
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io

class GenkouYooshiGenerator:
    def __init__(self, font_path=None):
        """
        Initialize the generator.
        
        Args:
            font_path: Path to a Japanese font file (TTF). If None, uses system default.
        """
        self.page_width, self.page_height = A4
        self.margin = 20 * mm
        self.grid_size = 10 * mm  # Standard genkō yōshi square size
        self.font_size = 24       # Increase font size for better fit
        
        # Always use Japanese font from folder if not specified
        if not font_path:
            font_path = str(Path(__file__).parent / "DFKyoKaSho-W4.ttf")
        if Path(font_path).exists():
            pdfmetrics.registerFont(TTFont('Japanese', font_path))
            self.font_name = 'Japanese'
        else:
            # Fallback to Helvetica (may not display Japanese properly)
            self.font_name = 'Helvetica'
            print("Warning: No Japanese font specified. Characters may not display correctly.")
    
    def extract_from_txt(self, txt_path):
        """
        Extract Japanese sentences from text file.
        
        Args:
            txt_path: Path to text file
            
        Returns:
            List of Japanese sentences
        """
        sentences = []
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Extract sentences from the content
                sentences = self._extract_sentences(content)
                
                # Filter to keep only sentences with Japanese characters
                sentences = [s for s in sentences if self._contains_japanese(s)]
                
        except Exception as e:
            print(f"Error reading text file: {e}")
        
        seen = set()
        ordered_sentences = []
        for s in sentences:
            if s not in seen:
                ordered_sentences.append(s)
                seen.add(s)
        return ordered_sentences    # Remove duplicates but keep original order
    
    def extract_from_string(self, text):
        """
        Extract Japanese sentences from a string.
        
        Args:
            text: Input string
            
        Returns:
            List of Japanese sentences
        """
        sentences = self._extract_sentences(text)
        sentences = [s for s in sentences if self._contains_japanese(s)]
        seen = set()
        ordered_sentences = []
        for s in sentences:
            if s not in seen:
                ordered_sentences.append(s)
                seen.add(s)
        return ordered_sentences
    
    def _contains_japanese(self, text):
        """Check if text contains Japanese characters."""
        japanese_pattern = r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]'
        return bool(re.search(japanese_pattern, text))
    
    def _extract_sentences(self, text):
        """Extract individual sentences from text."""
        # Clean up the text first
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        # Split and keep punctuation (。！？)
        sentences = re.findall(r'.+?[。！？]', text)

        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 1:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def create_worksheet(self, sentences, output_path, 
                        title="Japanese Handwriting Practice",
                        rows_per_page=30):
        """
        Create a genkō yōshi worksheet PDF.
        
        Args:
            sentences: List of Japanese sentences
            output_path: Output PDF file path
            title: Worksheet title
            rows_per_page: Number of rows per page
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        
        # Calculate grid dimensions
        cols_per_row = int((self.page_width - 2 * self.margin) // self.grid_size)
        
        current_row = 0
        page_num = 1
        
        for sentence in sentences:
             # Calculate required rows for this sentence
            chars = len(sentence)
            example_rows = (chars - 1) // cols_per_row + 1
            practice_rows = ((chars * 2) - 1) // cols_per_row + 1
            total_rows = example_rows + practice_rows
            
            # Check if we need a new page
            if current_row + total_rows >= rows_per_page:
                self._add_page_number(c, page_num)
                c.showPage()
                current_row = 0
                page_num += 1
            
            # Add title on first page
            if current_row == 0 and page_num == 1:
                self._add_title(c, title)
                current_row += 1  # Skip some rows for title
            
            # Skip a row before each new sentence for line break
            current_row += 1

            # Add sentence
            self._add_sentence_to_grid(c, sentence, current_row, cols_per_row)
            current_row += total_rows  # One row for characters, one for practice
        
        # Add final page number
        self._add_page_number(c, page_num)
        c.save()
        print(f"Worksheet created: {output_path}")
    
    def _add_title(self, c, title):
        """Add title to the page."""
        c.setFont('Helvetica-Bold', 18)
        title_width = c.stringWidth(title, 'Helvetica-Bold', 18)
        x = (self.page_width - title_width) / 2
        y = self.page_height - self.margin - 15 * mm
        c.drawString(x, y, title)
    
    def _add_page_number(self, c, page_num):
        """Add page number."""
        c.setFont('Helvetica', 10)
        c.drawString(self.page_width - self.margin - 20 * mm, 
                    self.margin - 10 * mm, f"Page {page_num}")
    
    def _add_sentence_to_grid(self, c, sentence, start_row, cols_per_row):
        """Add a sentence to the genkō yōshi grid."""
        chars = len(sentence)
        example_rows = (chars - 1) // cols_per_row + 1

        # First, draw the example characters
        self._draw_characters_in_grid(c, sentence, start_row, cols_per_row, True)
        
        # First practice row: draw example sentence in grey for tracing
        c.setFillColorRGB(0.7, 0.7, 0.7)  # Set grey color
        self._draw_characters_in_grid(c, sentence, start_row + example_rows, cols_per_row, True)
        c.setFillColorRGB(0, 0, 0)        # Reset to black
        
        # Second practice row: draw empty grid for practice
        #self._draw_empty_grid(c, chars, start_row + example_rows + ((chars - 1) // cols_per_row + 1), cols_per_row)
        self._draw_empty_grid(c, chars, start_row + example_rows*2, cols_per_row)
    
    def _draw_characters_in_grid(self, c, text, row, cols_per_row, with_characters=True):
        """Draw characters in genkō yōshi grid format."""
        c.setFont(self.font_name, self.font_size)
        
        for i, char in enumerate(text):
            if char.isspace():
                continue
                
            col = i % cols_per_row
            actual_row = row + (i // cols_per_row)
            
            # Calculate position
            x = self.margin + col * self.grid_size
            y = self.page_height - self.margin - (actual_row + 1) * self.grid_size
            
            # Draw grid square
            c.rect(x, y, self.grid_size, self.grid_size)
            
            # Draw center lines for character guidance
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.setLineWidth(0.5)
            c.setDash(2, 2)  # Dotted line: 2 points on, 2 points off
            c.line(x + self.grid_size/2, y, x + self.grid_size/2, y + self.grid_size)
            c.line(x, y + self.grid_size/2, x + self.grid_size, y + self.grid_size/2)
            c.setDash()  # Reset to solid for other lines
            c.setLineWidth(1)
            c.setStrokeColorRGB(0, 0, 0)
            
            # Add character if requested
            if with_characters:
                char_width = c.stringWidth(char, self.font_name, self.font_size)
                char_x = x + (self.grid_size - char_width) / 2
                char_y = y + self.grid_size/2 - self.font_size/3
                c.drawString(char_x, char_y, char)
    
    def _draw_empty_grid(self, c, char_count, row, cols_per_row):
        """Draw empty genkō yōshi grid for practice."""
        for i in range(char_count):
            col = i % cols_per_row
            actual_row = row + (i // cols_per_row)
            
            # Calculate position
            x = self.margin + col * self.grid_size
            y = self.page_height - self.margin - (actual_row + 1) * self.grid_size
            
            # Draw grid square
            c.rect(x, y, self.grid_size, self.grid_size)
            
            # Draw center lines
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.setLineWidth(0.5)
            c.setDash(2, 2)  # Dotted line: 2 points on, 2 points off
            c.line(x + self.grid_size/2, y, x + self.grid_size/2, y + self.grid_size)
            c.line(x, y + self.grid_size/2, x + self.grid_size, y + self.grid_size/2)
            c.setDash()  # Reset to solid for other lines
            c.setLineWidth(1)
            c.setStrokeColorRGB(0, 0, 0)


def main():
    parser = argparse.ArgumentParser(description="Generate genkō yōshi handwriting worksheets from Japanese text")
    parser.add_argument('txt_file', help='Path to text file with Japanese sentences')
    parser.add_argument('--font-path', help='Path to Japanese font file (TTF)')
    parser.add_argument('--output', '-o', default='handwriting_practice.pdf', help='Output PDF file path')
    parser.add_argument('--title', default='Japanese Handwriting Practice', help='Worksheet title')
    parser.add_argument('--max-sentences', type=int, help='Maximum number of sentences to include')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = GenkouYooshiGenerator(args.font_path)
    
    # Extract sentences
    sentences = generator.extract_from_txt(args.txt_file)
    
    if not sentences:
        print("No Japanese sentences found in the text file.")
        return
    
    # Limit sentences if requested
    if args.max_sentences:
        sentences = sentences[:args.max_sentences]
    
    print(f"Found {len(sentences)} sentences. Generating worksheet...")
    
    # Create worksheet
    generator.create_worksheet(sentences, args.output, args.title)

def generate_pdf_from_string(text, output_path=None, font_path=None, title="Japanese Handwriting Practice", max_sentences=None):
    generator = GenkouYooshiGenerator(font_path)
    sentences = generator.extract_from_string(text)
    if not sentences:
        print("No Japanese sentences found.")
        return None
    if max_sentences:
        sentences = sentences[:max_sentences]
    buffer = io.BytesIO()
    generator.create_worksheet(sentences, buffer, title)
    pdf_data = buffer.getvalue()
    buffer.close()
    # Optionally save to file if output_path is provided
    if output_path:
        with open(output_path, "wb") as f:
            f.write(pdf_data)
    return pdf_data


if __name__ == "__main__":
    main()
