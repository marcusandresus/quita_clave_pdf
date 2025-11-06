"""
PDF UNLOCKER SCRIPT
A command-line utility to decrypt password-protected PDF files
and save an unencrypted copy. It uses the PyPDF2 library.
"""

import argparse
import os

import PyPDF2


def decrypt_and_save(input_filepath, output_filepath, password):
    """
    Attempts to decrypt a PDF file using the given password and saves a new
    unencrypted copy to the specified output path.

    :param input_filepath: Path to the password-protected PDF file.
    :param output_filepath: Path where the unencrypted PDF will be saved.
    :param password: The current password of the input PDF.
    :return: True if decryption and saving were successful, False otherwise.
    """
    try:
        # Open the PDF file in binary mode
        with open(input_filepath, "rb") as input_file:
            reader = PyPDF2.PdfReader(input_file)

            # Check if the file is encrypted
            if reader.is_encrypted:
                # Attempt to decrypt with the provided password
                if reader.decrypt(password):
                    writer = PyPDF2.PdfWriter()

                    # Copy all pages to the new writer
                    for page in reader.pages:
                        writer.add_page(page)

                    # Save the new unencrypted PDF
                    with open(output_filepath, "wb") as output_file:
                        writer.write(output_file)

                    print(
                        f"✅ Success: Unencrypted copy saved to **{output_filepath}**"
                    )
                    return True
                else:
                    print(
                        f"❌ Error: Provided password is NOT correct for **{input_filepath}**"
                    )
                    return False
            else:
                print(
                    f"⚠️ Warning: File **{input_filepath}** was NOT encrypted. Skipping save."
                )
                return True

    except FileNotFoundError:
        print(f"❌ Error: Input file not found at **{input_filepath}**")
    except Exception as e:
        print(f"❌ An unexpected error occurred while processing the file: {e}")
    return False


def main():
    """
    Main function to parse command-line arguments and run the decryption process.
    """
    parser = argparse.ArgumentParser(
        description="Decrypts a password-protected PDF file and saves an unencrypted copy."
    )

    # Required positional arguments
    parser.add_argument(
        "input_file",
        type=str,
        help="The path to the input password-protected PDF file.",
    )
    parser.add_argument(
        "password",
        type=str,
        help="The password required to decrypt the input PDF file.",
    )

    # Optional argument for output file name
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Optional path for the output file. If omitted, '.unlocked' is added before the '.pdf' extension.",
    )

    args = parser.parse_args()

    # Determine the output file path based on the user input or default rule
    if args.output:
        output_name = args.output
    else:
        # Default rule: Add ".unlocked" before the .pdf extension
        base, ext = os.path.splitext(args.input_file)
        if ext.lower() != ".pdf":
            # Handle cases where the file might not strictly end in .pdf (though rare for bills)
            output_name = f"{args.input_file}.unlocked.pdf"
        else:
            output_name = f"{base}.unlocked{ext}"

    # Run the decryption function
    decrypt_and_save(args.input_file, output_name, args.password)


if __name__ == "__main__":
    main()
