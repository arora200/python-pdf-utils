# PDF Utilities

This project provides Python scripts to efficiently remove pages from PDF files. It includes two different implementations using popular libraries: `PyPDF2` and `PyMuPDF`.

## Features

*   **Memory Efficient:** Scripts are designed to handle large PDF files without loading them entirely into memory.
*   **Page Validation:** Ensures that the specified page numbers are valid for the given PDF, preventing errors.
*   **Metadata Preservation:** The original PDF's metadata (like author, title, etc.) is preserved in the output file.
*   **Progress Indicators:** Displays a progress bar to show the status of page processing.
*   **Duplicate Page Handling:** Automatically handles duplicate page numbers provided for removal.

## Implementations

This project offers two scripts with different underlying libraries for PDF manipulation:

1.  `logicOne.py`: Uses the `PyPDF2` library.
2.  `logicTwo.py`: Uses the `PyMuPDF` (Fitz) library, which is generally faster for this task.

## Requirements

The required Python libraries are listed in the `requirements.txt` file. You can install them using pip:

```bash
pip install -r requirements.txt
```

## Usage

Both scripts can be run from the command line and accept similar arguments.

### `logicOne.py` (PyPDF2)

```bash
python logicOne.py <input_pdf> <output_pdf> -p <page1> <page2> ...
```

**Example:**

To remove pages 1, 2, and 546 from a PDF:

```bash
python logicOne.py data/NCRB_STATS.pdf temp/filtered_NCRB_STATS_logicOne.pdf -p 1 2 546
```

### `logicTwo.py` (PyMuPDF)

```bash
python logicTwo.py <input_pdf> <output_pdf> -p <page1> <page2> ...
```

**Example:**

To remove pages 1, 2, and 546 from a PDF:

```bash
python logicTwo.py data/NCRB_STATS.pdf temp/filtered_NCRB_STATS_logicTwo.pdf -p 1 2 546
```

### Page Indexing

By default, page numbers are treated as 1-indexed (the first page is page 1). You can use the `--zero-indexed` flag to treat them as 0-indexed (the first page is page 0).

**Example (0-indexed):**

```bash
python logicOne.py data/NCRB_STATS.pdf temp/filtered_output.pdf -p 0 1 545 --zero-indexed
```

## Contributing

Please see the `CONTRIBUTING.md` file for details on how to contribute to this project.

## License

This project is licensed under the terms of the `LICENSE` file.