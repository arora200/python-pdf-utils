import fitz  # PyMuPDF
import argparse
from pathlib import Path
from typing import List
from tqdm import tqdm

def remove_pages_fast(
    input_path: str,
    output_path: str,
    pages_to_remove: List[int],
    zero_indexed: bool = False
):
    """
    Remove specific pages from a PDF file using PyMuPDF.
    
    Args:
        input_path: Path to input PDF
        output_path: Path for output PDF
        pages_to_remove: List of page numbers to remove
        zero_indexed: False for human-friendly 1-indexing (page 1 = first page)
                     True for programming 0-indexing (page 0 = first page)
    """
    if not Path(input_path).exists():
        raise FileNotFoundError(f"Input PDF not found: {input_path}")

    print(f"📄 Opening PDF: {input_path}")
    doc = fitz.open(input_path)
    total_pages = len(doc)
    print(f"Total pages: {total_pages}")

    # Convert to 0-indexed and validate
    remove_set = set(p - 1 for p in pages_to_remove) if not zero_indexed else set(pages_to_remove)
    
    invalid = [p for p in remove_set if p < 0 or p >= total_pages]
    if invalid:
        raise ValueError(f"❌ Invalid pages {sorted(invalid)}. PDF has pages 1-{total_pages}")

    # Sort in reverse order to avoid issues with page re-indexing during deletion
    sorted_pages_to_remove = sorted(list(remove_set), reverse=True)
    
    print("Removing pages...")
    for page_num in tqdm(sorted_pages_to_remove, desc="Deleting pages"):
        doc.delete_page(page_num)
    
    doc.save(output_path)
    doc.close()
    print(f"\n✅ Success! Created: {output_path}")
    print(f"   Original pages: {total_pages}")
    print(f"   Pages removed: {len(remove_set)}")
    print(f"   Final pages: {total_pages - len(remove_set)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove specific pages from a PDF file using PyMuPDF.")
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
        remove_pages_fast(
            args.input_pdf,
            args.output_pdf,
            args.pages_to_remove,
            args.zero_indexed
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")