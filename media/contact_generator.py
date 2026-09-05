#!/usr/bin/env python3
"""
Generate contact VCF files.
Combines conta.py and utils.py.
"""
import random
import json
from pathlib import Path
from multiprocessing import Pool, cpu_count
from typing import List, Dict, Any

class ContactGenerator:
    """Generate VCF contact files."""
    
    def __init__(self, start: int = 10000000, end: int = 99999999, step: int = 47):
        self.start = start
        self.end = end
        self.step = step
        self.chunk_size = 100000
    
    def generate_vcf(self, phone: int, name: str = "") -> str:
        """Generate a single VCF contact."""
        if name:
            return f"BEGIN:VCARD\nVERSION:2.1\nN:{name};;;;\nFN:{name}\nTEL;CELL:+2519{phone}\nEND:VCARD\n"
        return f"BEGIN:VCARD\nVERSION:2.1\nTEL;CELL:+2519{phone}\nEND:VCARD\n"
    
    def generate_chunk(self, start: int) -> str:
        """Generate a chunk of contacts."""
        end = min(start + self.chunk_size * self.step, self.end)
        contacts = []
        
        for phone in range(start, end, self.step):
            if random.random() < 0.2:  # 20% named
                name = f"User{phone % 10000}"
                contacts.append(self.generate_vcf(phone, name))
            else:
                contacts.append(self.generate_vcf(phone))
        
        return ''.join(contacts)
    
    def generate(self, output_file: str = "contacts.vcf", count: int = 10000) -> None:
        """Generate contacts file."""
        output = Path(output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # Adjust chunk size for desired count
        self.chunk_size = max(1, count // cpu_count())
        
        with open(output, 'w', encoding='utf-8') as f:
            with Pool(processes=cpu_count()) as pool:
                chunks = range(self.start, self.end, self.chunk_size * self.step)
                for result in pool.imap(self.generate_chunk, chunks, chunksize=4):
                    f.write(result)
        
        print(f"Generated contacts: {output}")
    
    def filter_no_name(self, input_file: str, output_file: str = None) -> None:
        """Remove contacts without names."""
        input_path = Path(input_file)
        if not output_file:
            output_file = input_path.with_suffix(input_path.suffix + '.filtered')
        
        content = input_path.read_text(encoding='utf-8')
        
        # Find contacts without names
        pattern = re.compile(r'BEGIN:VCARD\nVERSION:2.1\nTEL;CELL:\+2519\d{8}\nEND:VCARD')
        no_name = pattern.findall(content)
        
        for contact in no_name:
            content = content.replace(contact, "")
        
        Path(output_file).write_text(content, encoding='utf-8')
        print(f"Filtered {len(no_name)} contacts, saved to {output_file}")

def main():
    import sys
    generator = ContactGenerator()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'filter':
        generator.filter_no_name(sys.argv[2] if len(sys.argv) > 2 else 'contacts.vcf')
    else:
        count = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
        generator.generate(count=count)

if __name__ == "__main__":
    main()
