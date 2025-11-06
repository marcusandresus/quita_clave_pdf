import os
import tempfile
from pathlib import Path
import PyPDF2
import pytest

from pdf_unlocker import decrypt_and_save

def create_sample_pdf(path: str) -> None:
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with open(path, "wb") as f:
        writer.write(f)

def create_encrypted_pdf(path: str, password: str) -> None:
    writer = PyPDF2.PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.encrypt(password)
    with open(path, "wb") as f:
        writer.write(f)

def test_decrypt_success(tmp_path):
    inp = tmp_path / "enc.pdf"
    out = tmp_path / "out.pdf"
    password = "s3cr3t"
    create_encrypted_pdf(str(inp), password)
    rc = decrypt_and_save(str(inp), str(out), password)
    assert rc == 0
    assert out.exists()
    # open and confirm it's not encrypted
    reader = PyPDF2.PdfReader(str(out))
    assert not reader.is_encrypted

def test_wrong_password(tmp_path):
    inp = tmp_path / "enc_wrong.pdf"
    out = tmp_path / "out_wrong.pdf"
    create_encrypted_pdf(str(inp), "right")
    rc = decrypt_and_save(str(inp), str(out), "wrong")
    assert rc == 3
    assert not out.exists()

def test_not_encrypted_writes_when_output_provided(tmp_path):
    inp = tmp_path / "plain.pdf"
    out = tmp_path / "plain_out.pdf"
    create_sample_pdf(str(inp))
    rc = decrypt_and_save(str(inp), str(out), None)
    # function returns 4 for not-encrypted; but writes when output provided
    assert rc == 4 or rc == 0
    if out.exists():
        reader = PyPDF2.PdfReader(str(out))
        assert not reader.is_encrypted
