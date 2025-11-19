import fitz  # PyMuPDF
import argparse
import json
import os

def get_common_font_size(spans):
    """Calculate the most common font size from a list of spans."""
    if not spans:
        return 0
    font_sizes = [span['size'] for span in spans]
    return max(set(font_sizes), key=font_sizes.count) if font_sizes else 0

def is_bold(spans):
    """Check if the font is bold."""
    if not spans:
        return False
    # A simple heuristic: check if 'bold' is in the font name of the first span.
    # This can be improved with more sophisticated font analysis.
    font_name = spans[0]['font'].lower()
    return 'bold' in font_name or 'black' in font_name

def to_markdown(doc):
    """Convert PDF document to Markdown with ToC, improved heading detection, and table conversion."""
    
    # Extract Table of Contents
    toc = doc.get_toc()
    toc_content = "## Table of Contents\n\n"
    if toc:
        for level, title, page in toc:
            indent = "  " * (level - 1)
            toc_content += f"{indent}- [{title}](#page-{page})\n"
        toc_content += "\n"
    else:
        toc_content = "## Table of Contents\n\n_No table of contents found._\n\n"

    markdown_content = toc_content

    # Analyze font sizes for heading hierarchy
    font_sizes = {}
    for page in doc:
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)['blocks']
        for b in blocks:
            if b['type'] == 0:
                for l in b['lines']:
                    for s in l['spans']:
                        size = round(s['size'])
                        font_sizes[size] = font_sizes.get(size, 0) + len(s['text'])

    sorted_sizes = sorted(font_sizes.keys(), reverse=True)
    h_levels = {size: "#" * (i + 1) for i, size in enumerate(sorted_sizes[:4])}

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        page_markdown = f"<a name='page-{page_num + 1}'></a>\n"
        page_markdown += f"## Page {page_num + 1}\n\n"

        # Find and process tables first
        tables = page.find_tables()
        table_bboxes = [fitz.Rect(t.bbox) for t in tables]

        for i, table in enumerate(tables):
            page_markdown += "### Table\n"
            try:
                tab_data = table.extract()
                if tab_data:
                    header = [str(item) if item else "" for item in tab_data[0]]
                    page_markdown += f"| {' | '.join(header)} |\n"
                    page_markdown += f"|{'|'.join(['---'] * len(header))}|\n"
                    for row in tab_data[1:]:
                        data = [str(item) if item else "" for item in row]
                        page_markdown += f"| {' | '.join(data)} |\n"
                    page_markdown += "\n"
            except Exception as e:
                page_markdown += f"_Could not extract table: {e}_\n\n"

        # Process text blocks, skipping those inside tables
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)['blocks']
        for block in blocks:
            if block['type'] == 0:  # Text block
                block_rect = fitz.Rect(block['bbox'])
                in_table = any(block_rect.intersects(t_bbox) for t_bbox in table_bboxes)
                if in_table:
                    continue

                for line in block['lines']:
                    line_text = "".join(span['text'] for span in line['spans']).strip()
                    if not line_text:
                        continue

                    spans = line['spans']
                    common_size = round(get_common_font_size(spans))
                    bold = is_bold(spans)
                    all_caps = line_text.isupper() and len(line_text) > 1

                    if common_size in h_levels:
                        page_markdown += f"{h_levels[common_size]} {line_text}\n"
                    elif bold and all_caps:
                        page_markdown += f"#### {line_text}\n"
                    elif bold:
                        page_markdown += f"**{line_text}**\n"
                    else:
                        page_markdown += line_text + "\n"
                page_markdown += "\n"
        
        markdown_content += page_markdown
    return markdown_content

def to_text(doc):
    """Convert PDF document to plain text."""
    text_content = ""
    for page in doc:
        text_content += page.get_text()
        text_content += "\n--- End of Page ---\n"
    return text_content

def to_json(doc):
    """Convert PDF document to JSON with structured data."""
    pdf_json = {
        "metadata": doc.metadata,
        "num_pages": len(doc),
        "pages": []
    }
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)
        
        page_data = {
            "page_number": page_num + 1,
            "blocks": blocks.get('blocks', [])
        }
        pdf_json["pages"].append(page_data)
        
    return json.dumps(pdf_json, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to various formats.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_path", help="Path to the output file.")
    parser.add_argument("-f", "--format", choices=['md', 'txt', 'json'], required=True,
                        help="Output format: 'md' (Markdown), 'txt' (Text), 'json' (JSON).")
    
    args = parser.parse_args()

    if not os.path.exists(args.input_pdf):
        print(f"Error: Input PDF not found at '{args.input_pdf}'")
        return

    try:
        doc = fitz.open(args.input_pdf)
    except Exception as e:
        print(f"Error opening or processing PDF: {e}")
        return

    output_content = ""
    if args.format == 'md':
        output_content = to_markdown(doc)
    elif args.format == 'txt':
        output_content = to_text(doc)
    elif args.format == 'json':
        output_content = to_json(doc)

    try:
        with open(args.output_path, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"Successfully converted '{args.input_pdf}' to '{args.output_path}' as {args.format.upper()}.")
    except Exception as e:
        print(f"Error writing to output file: {e}")
    finally:
        doc.close()

if __name__ == "__main__":
    main()
