#!/usr/bin/env python3
"""
transcribe_notes.py — Convert scanned handwritten PDF notes to text using Claude.

Usage:
    python3 transcribe_notes.py /path/to/folder/of/pdfs

Requirements:
    pip install anthropic pymupdf

The script will:
  - Find all PDFs in the given folder
  - Convert each page to an image
  - Send each page to Claude Haiku for transcription
  - Save one .txt file per PDF into the same folder as this script

Your Anthropic API key must be set as an environment variable:
    export ANTHROPIC_API_KEY="sk-ant-..."
"""

import sys
import os
import base64
import anthropic
import fitz  # pymupdf

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL      = "claude-haiku-4-5-20251001"
DPI        = 150  # higher = better quality but larger images


def transcribe_page(client, img_bytes):
    img_b64 = base64.standard_b64encode(img_bytes).decode()
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_b64
                    }
                },
                {
                    "type": "text",
                    "text": (
                        "Transcribe all handwritten text from this page exactly as written. "
                        "Preserve the structure and layout as best you can. "
                        "Output only the transcribed text — no commentary, no labels."
                    )
                }
            ]
        }]
    )
    return response.content[0].text


def transcribe_pdf(client, pdf_path):
    doc  = fitz.open(pdf_path)
    name = os.path.splitext(os.path.basename(pdf_path))[0]
    print(f"  Processing {name}.pdf ({doc.page_count} pages)...")

    pages = []
    for i, page in enumerate(doc, start=1):
        print(f"    Page {i}/{doc.page_count}", end="\r")
        pix      = page.get_pixmap(dpi=DPI)
        img_bytes = pix.tobytes("png")
        text     = transcribe_page(client, img_bytes)
        pages.append(text)

    print()  # newline after progress indicator
    return "\n\n---\n\n".join(pages)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_notes.py /path/to/pdf/folder")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a folder.")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Run: export ANTHROPIC_API_KEY=\"your-key-here\"")
        sys.exit(1)

    pdfs = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    if not pdfs:
        print(f"No PDF files found in '{folder}'.")
        sys.exit(1)

    print(f"Found {len(pdfs)} PDF(s) in '{folder}'.\n")
    client = anthropic.Anthropic(api_key=api_key)

    for pdf_file in sorted(pdfs):
        pdf_path = os.path.join(folder, pdf_file)
        try:
            text     = transcribe_pdf(client, pdf_path)
            out_name = os.path.splitext(pdf_file)[0] + ".txt"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  Saved: {out_path}\n")
        except Exception as e:
            print(f"  Error processing {pdf_file}: {e}\n")

    print("Done.")


if __name__ == "__main__":
    main()
