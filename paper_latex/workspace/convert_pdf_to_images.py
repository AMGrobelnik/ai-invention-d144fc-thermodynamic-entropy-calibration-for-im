#!/usr/bin/env python3
"""Convert PDF pages to PNG images for visual review."""
import os
import subprocess
import sys

# Try to use pdf2image first, fallback to pymupdf
output_dir = "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/page_images"
os.makedirs(output_dir, exist_ok=True)

pdf_path = "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.pdf"

# Try using pdftoppm (poppler-utils) for fast conversion
try:
    # Convert PDF to PNG at 150 DPI using pdftoppm
    cmd = f"pdftoppm -png -r 150 {pdf_path} {output_dir}/page"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully converted PDF to PNG using pdftoppm")
    else:
        print(f"pdftoppm failed: {result.stderr}")
        # Try pymupdf as fallback
        try:
            import fitz
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                mat = fitz.Matrix(150/72, 150/72)  # 150 DPI
                pix = page.get_pixmap(matrix=mat)
                output_path = os.path.join(output_dir, f"page-{page_num+1:02d}.png")
                pix.save(output_path)
            print(f"Successfully converted PDF to PNG using pymupdf")
        except ImportError:
            print("pymupdf not available, trying pdf2image...")
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(pdf_path, dpi=150)
                for i, image in enumerate(images):
                    output_path = os.path.join(output_dir, f"page-{i+1:02d}.png")
                    image.save(output_path, "PNG")
                print(f"Successfully converted PDF to PNG using pdf2image")
            except ImportError:
                print("ERROR: No PDF to image conversion tool available")
                sys.exit(1)
except Exception as e:
    print(f"Error during conversion: {e}")
    sys.exit(1)

# List generated images
images = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])
print(f"\nGenerated {len(images)} page images:")
for img in images:
    img_path = os.path.join(output_dir, img)
    size = os.path.getsize(img_path)
    print(f"  {img}: {size/1024:.1f} KB")
