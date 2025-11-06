# 🔒 PDF Unlocker Utility (`pdf_unlocker.py`)

## 📝 Description

`pdf_unlocker.py` is a simple command-line Python utility designed to **decrypt (remove the password)** from protected PDF files. This is particularly useful for batches of automated documents (like bills or invoices) that use predictable, but varied, passwords (such as a RUT or part of a document ID).

The script takes the input file path and the correct password, then saves a new, unencrypted copy of the document, leaving the original file untouched. It is built using the standard Python module `argparse` for command-line handling and the powerful `PyPDF2` library for PDF manipulation.

## ⚙️ Prerequisites

1.  **Python 3**: Ensure you have Python 3 installed on your system.
2.  **PyPDF2 Library**: Install the required library using pip:

    ```bash
    pip install PyPDF2
    ```

## 🚀 How to Use

The script requires **two positional arguments** (the input file and the password) and accepts **one optional argument** (`-o` or `--output`).

### 1. Basic Usage (Automatic Output Name)

To run the script, provide the file path and the password. If the output name is not specified, the script automatically generates the output file name by appending `.unlocked` before the `.pdf` extension.

**Syntax:**

```bash
python pdf_unlocker.py <INPUT_FILE> <PASSWORD>
```
