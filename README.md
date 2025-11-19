# PDF Processing Utilities

This project provides a suite of powerful Python scripts for advanced PDF processing. It allows you to perform tasks such as removing pages from large files and converting PDFs into various formats like Markdown, plain text, and JSON, while preserving the original document's structure.

## Features

This project includes three main scripts, each with unique capabilities:

### `logicOne.py` & `logicTwo.py` (Page Removal)

These scripts are designed for efficiently removing specific pages from large PDF files.

*   **Memory Efficient:** Optimized for large files to minimize memory usage.
*   **Page Validation:** Verifies that all specified page numbers are valid for the given document.
*   **Metadata Preservation:** Keeps the original PDF metadata intact in the output file.
*   **Progress Indicators:** Shows a progress bar for long operations.
*   **Flexible Page Indexing:** Supports both 1-based (default) and 0-based page numbering.

### `logicThree.py` (PDF Conversion)

This is a highly advanced script for converting PDF files into other formats, with a focus on preserving the document's structure and content.

*   **Multiple Output Formats:** Convert PDFs to **Markdown (`.md`)**, **plain text (`.txt`)**, and **JSON (`.json`)**.
*   **Advanced Markdown Conversion:**
    *   **Table of Contents:** Automatically extracts the PDF's ToC and adds it to the start of the Markdown file with clickable page links.
    *   **Intelligent Heading Detection:** Uses font size, weight (bold), and capitalization to accurately identify and format headings.
    *   **Table Recognition:** Detects and converts tables from the PDF into proper Markdown table format.
*   **Structured JSON Output:** Creates a detailed JSON representation of the PDF, including text blocks, coordinates, and metadata.

## Requirements

All required Python libraries are listed in the `requirements.txt` file. Install them using pip:

```bash
pip install -r requirements.txt
```

## Usage

All scripts are run from the command line and accept arguments for input/output files and other options.

### Page Removal (`logicOne.py` & `logicTwo.py`)

To remove pages from a PDF, use the following syntax:

```bash
# Using PyPDF2
python logicOne.py <input_pdf> <output_pdf> -p <page1> <page2> ...

# Using PyMuPDF (generally faster)
python logicTwo.py <input_pdf> <output_pdf> -p <page1> <page2> ...
```

**Example:**

```bash
python logicTwo.py data/NCRB_STATS.pdf filtered_output.pdf -p 1 2 546
```

### PDF Conversion (`logicThree.py`)

To convert a PDF to a different format, use the following syntax:

```bash
python logicThree.py <input_pdf> <output_file> -f <format>
```

**Arguments:**

*   **`<format>`:** The desired output format. Choices are `md`, `txt`, or `json`.

**Examples:**

*   **To convert to Markdown:**
    ```bash
    python logicThree.py data/NCRB_STATS.pdf report.md -f md
    ```

*   **To convert to a Text file:**
    ```bash
    python logicThree.py data/NCRB_STATS.pdf report.txt -f txt
    ```

*   **To convert to a JSON file:**
    ```bash
    python logicThree.py data/NCRB_STATS.pdf report.json -f json
    ```

## Contributing

Please see the `CONTRIBUTING.md` file for details on how to contribute to this project.

## License

This project is licensed under the terms of the `LICENSE` file.
