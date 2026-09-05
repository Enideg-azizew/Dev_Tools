#!/usr/bin/env python3
"""
PDF processing tool with text extraction and TTS.
Based on aloud.py.
"""
import re
import subprocess
from pathlib import Path
from typing import Optional
import PyPDF2

class PDFTool:
    """Extract text from PDF and optionally read aloud."""
    
    def __init__(self, pdf_path: Optional[str] = None):
        self.pdf_path = Path(pdf_path) if pdf_path else None
        self.text = {}
    
    def extract_text(self, pdf_path: Optional[str] = None) -> dict:
        """Extract text from all pages."""
        path = Path(pdf_path) if pdf_path else self.pdf_path
        if not path or not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            
            for page_num, page in enumerate(reader.pages, 1):
                raw = page.extract_text()
                cleaned = self._clean_text(raw)
                self.text[page_num] = cleaned
        
        return self.text
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'\d+/\d+', '', text)
        return text.strip()
    
    def speak(self, text: str) -> bool:
        """Read text aloud using TTS."""
        try:
            # Try termux-tts-speak first
            subprocess.run(['termux-tts-speak', text], timeout=10)
            return True
        except:
            try:
                # Fallback to espeak
                subprocess.run(['espeak', text], timeout=10)
                return True
            except:
                return False
    
    def speak_page(self, page_num: int) -> bool:
        """Read a specific page aloud."""
        if page_num not in self.text:
            self.extract_text()
        return self.speak(self.text.get(page_num, ""))

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pdf_tool.py <pdf_file> [page_number]")
        sys.exit(1)
    
    tool = PDFTool(sys.argv[1])
    tool.extract_text()
    
    if len(sys.argv) > 2:
        tool.speak_page(int(sys.argv[2]))
    else:
        # Read all pages
        for text in tool.text.values():
            tool.speak(text)

if __name__ == "__main__":
    main()
