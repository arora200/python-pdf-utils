import PyPDF2
from pathlib import Path
from typing import List
import argparse
from tqdm import tqdm

def remove_pages_from_pdf(
    input_path: str,
    output_path: str,
    pages_to_remove: List[int],
    zero_indexed: bool = False
) -> dict:
    """
    Remove specific pages from a PDF file.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for output PDF
        pages_to_remove: List of page numbers to remove
        zero_indexed: False for human-friendly 1-indexing (page 1 = first page)
                     True for programming 0-indexing (page 0 = first page)
    
    Returns:
        dict: Processing statistics
    """
    # Validate input
    if not Path(input_path).exists():
        raise FileNotFoundError(f"Input PDF not found: {input_path}")
    
    print(f"📄 Opening PDF: {input_path}")
    
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        print(f"Total pages: {total_pages}")
        
        # Convert to 0-indexed and validate
        remove_set = set(p - 1 for p in pages_to_remove) if not zero_indexed else set(pages_to_remove)
        
        invalid = [p for p in remove_set if p < 0 or p >= total_pages]
        if invalid:
            raise ValueError(f"❌ Invalid pages {sorted(invalid)}. PDF has pages 1-{total_pages}")
        
        # Create new PDF
        writer = PyPDF2.PdfWriter()
        
        # Add pages with progress indicator
        for page_num in tqdm(range(total_pages), desc="Processing pages"):
            if page_num not in remove_set:
                writer.add_page(reader.pages[page_num])
        
        # Preserve metadata
        if reader.metadata:
            writer.add_metadata(reader.metadata)
        
        # Write output
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
    
    return {
        "original": total_pages,
        "removed": len(remove_set),
        "kept": total_pages - len(remove_set)
    }

# ========== USAGE EXAMPLE ==========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove specific pages from a PDF file.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_pdf", help="Path for the output PDF file.")
    parser.add_argument(
        "-p",
        "--pages-to-remove",
        nargs="+",
        type=int,
        required=True,
        help="List of page numbers to remove (1-indexed, e.g., 1 5 10)."
    )
    parser.add_argument(
        "--zero-indexed",
        action="store_true",
        help="Treat page numbers as 0-indexed instead of 1-indexed."
    )
    
    args = parser.parse_args()
    
    try:
        result = remove_pages_from_pdf(
            args.input_pdf,
            args.output_pdf,
            args.pages_to_remove,
            args.zero_indexed
        )
        
        print(f"\n✅ Success! Created: {args.output_pdf}")
        print(f"   Original pages: {result['original']}")
        print(f"   Pages removed: {result['removed']}")
        print(f"   Final pages: {result['kept']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")