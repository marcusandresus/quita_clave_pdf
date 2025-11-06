# PDF Unlocker

A small command-line utility to decrypt password-protected PDF files and save an unencrypted copy. The tool uses **PyPDF2** to read and write PDF files.

> **Note:** Use this tool only on PDFs you are authorized to decrypt. Please respect copyrights and privacy laws in your jurisdiction.

## Features / Purpose

- Detects whether a PDF is encrypted.
- Attempts to decrypt using a provided password.
- If decryption succeeds, writes an unencrypted copy of the PDF to disk.
- If the input file is not encrypted, the tool will report it and skip rewriting the file unless you explicitly provide an output file path.

## Prerequisites

- Python 3.8+ (tested with Python 3.8–3.11)
- `pip` to install dependencies
- `PyPDF2` Python package

Install the dependency with:

```bash
pip install PyPDF2
```

## Installation

1. Download the repository and extract it (or clone it).
2. Ensure `pdf_unlocker.py` is executable or run it with `python`.

## Usage

```bash
python pdf_unlocker.py <input_file.pdf> <password> [--output OUTPUT]
```

Arguments:

- `<input_file.pdf>` — Path to the password-protected PDF.
- `<password>` — Password to decrypt the PDF.
- `-o, --output OUTPUT` — Optional path for the output (unencrypted) PDF. If omitted, the script adds `.unlocked` before the `.pdf` extension of the input file (e.g. `document.pdf` → `document.unlocked.pdf`). If the input filename does not end in `.pdf`, the script will append `.unlocked.pdf` to the existing name.

### Examples

1. Default output name (adds `.unlocked` before the extension):

```bash
python pdf_unlocker.py secret.pdf MyPassword123
# Output file: secret.unlocked.pdf
```

2. Explicit output path:

```bash
python pdf_unlocker.py secret.pdf MyPassword123 -o /tmp/secret_plain.pdf
```

3. Input file without `.pdf` extension (rare):

```bash
python pdf_unlocker.py invoice_2025 MyPassword123
# Output file: invoice_2025.unlocked.pdf
```

## Exit behavior and messages

- Prints success message when an unencrypted copy is written.
- Prints an error message and returns `False` from the core function when the password is incorrect or when an unexpected error occurs.
- If the file is not encrypted, it prints a warning and returns success (`True`) without writing a new file — unless you passed an output path, in which case the script currently still skips writing and only reports that the file was not encrypted.

## Code notes and suggestions

- `PyPDF2.PdfReader.decrypt()` historically returned an integer (0 for failure, 1 for success) in older versions — newer versions may return `True`/`False`. The script treats any truthy return value as success.
- The script currently prints messages with emoji. If you plan to use it in automation or CI, consider replacing `print()` with logging and using process exit codes (e.g. `sys.exit(0)` / `sys.exit(1)`) to indicate success/failure for other programs.
- If you want the script to always write an output file when `--output` is provided, modify the branch that handles a non-encrypted input to still copy pages and write them out.
- The script does not implement password brute-forcing — you must provide the correct password.

## Legal & Ethical

Only use this script on PDF documents for which you have permission to remove encryption (e.g., your own documents or documents you are authorized to manage). Removing encryption from files you do not have rights to may be illegal in your jurisdiction.

## License

This project is released under the BSD 3-Clause License. See the `LICENSE` file for full text.


## Tests

This repository includes basic pytest tests that create small PDFs (encrypted and unencrypted)
and verify the behavior of `decrypt_and_save`. To run tests:

```bash
pip install pytest PyPDF2
pytest
```

## Packaging / Installation

This project includes `pyproject.toml` and `setup.cfg` to build and install the package.
To install locally in editable mode (development):

```bash
pip install -e .
```

After installation the CLI entry point `pdf-unlocker` will be available (see `setup.cfg`).
