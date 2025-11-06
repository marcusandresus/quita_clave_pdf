#!/usr/bin/env python3
"""
PDF Unlocker - improved
A command-line utility to decrypt password-protected PDF files
and save an unencrypted copy. Uses PyPDF2 for PDF operations.
This version uses logging, explicit exit codes and is safer for automation.
"""

from __future__ import annotations
import argparse
import os
import sys
import logging
from typing import Optional

import PyPDF2


# Exit codes
EXIT_OK = 0
EXIT_GENERAL_ERROR = 1
EXIT_FILE_NOT_FOUND = 2
EXIT_WRONG_PASSWORD = 3
EXIT_NOT_ENCRYPTED = 4

logger = logging.getLogger("pdf_unlocker")


def decrypt_and_save(input_filepath: str, output_filepath: str, password: Optional[str]) -> int:
    """
    Attempts to decrypt a PDF file using the given password and saves a new
    unencrypted copy to the specified output path.

    Returns an exit code (int):
      - 0: success (file written or input not encrypted and no-op)
      - 2: input file not found
      - 3: wrong password
      - 1: general error
    """
    try:
        if not os.path.exists(input_filepath):
            logger.error("Input file not found: %s", input_filepath)
            return EXIT_FILE_NOT_FOUND

        with open(input_filepath, "rb") as input_file:
            reader = PyPDF2.PdfReader(input_file)

            if not reader.is_encrypted:
                logger.warning("Input file was NOT encrypted: %s", input_filepath)
                # If user requested an explicit output, write a copy; otherwise no-op.
                if output_filepath:
                    writer = PyPDF2.PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    with open(output_filepath, "wb") as out_f:
                        writer.write(out_f)
                    logger.info("Unencrypted copy written to: %s", output_filepath)
                    return EXIT_OK
                return EXIT_NOT_ENCRYPTED

            # Attempt decryption; PyPDF2.decrypt may return bool or int depending on version
            decrypted = reader.decrypt(password or "")
            if not decrypted:
                logger.error("Provided password is NOT correct for: %s", input_filepath)
                return EXIT_WRONG_PASSWORD

            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with open(output_filepath, "wb") as output_file:
                writer.write(output_file)

            logger.info("Success: Unencrypted copy saved to %s", output_filepath)
            return EXIT_OK

    except FileNotFoundError:
        logger.error("Input file not found exception: %s", input_filepath)
        return EXIT_FILE_NOT_FOUND
    except Exception as exc:
        logger.exception("An unexpected error occurred while processing the file: %s", exc)
        return EXIT_GENERAL_ERROR


def configure_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        root.addHandler(handler)
    root.setLevel(level)


def build_output_name(input_file: str, explicit_output: Optional[str]) -> str:
    if explicit_output:
        return explicit_output
    base, ext = os.path.splitext(input_file)
    if ext.lower() != ".pdf":
        return f"{input_file}.unlocked.pdf"
    return f"{base}.unlocked{ext}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Decrypts a password-protected PDF file and saves an unencrypted copy."
    )
    parser.add_argument("input_file", type=str, help="Path to the input password-protected PDF file.")
    parser.add_argument("password", type=str, nargs="?", default=None, help="Password to decrypt the PDF (optional).")
    parser.add_argument("-o", "--output", type=str, default=None, help="Optional output file path.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")

    args = parser.parse_args()
    configure_logging(logging.DEBUG if args.debug else logging.INFO)

    output_name = build_output_name(args.input_file, args.output)

    exit_code = decrypt_and_save(args.input_file, output_name, args.password)

    # Map internal "not encrypted" exit code to success if desired; keep distinct for callers
    if exit_code == EXIT_OK:
        sys.exit(EXIT_OK)
    elif exit_code == EXIT_NOT_ENCRYPTED:
        # Not encrypted but not an error; exit code 0 but log informs the caller
        logger.info("Input was not encrypted; no decryption performed.")
        sys.exit(EXIT_OK)
    else:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
