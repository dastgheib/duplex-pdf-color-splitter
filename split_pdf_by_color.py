#!/usr/bin/env python3
import fitz  # pip install pymupdf
import argparse

def detect_color_pages(src_doc, start, sample_count=1000):
    """Return list of page-indices ≥ start that contain color."""
    color_pages = []
    total = src_doc.page_count
    for i in range(start, total):
        page = src_doc.load_page(i)
        pix = page.get_pixmap(alpha=False)  # render at default resolution
        w, h, n = pix.width, pix.height, pix.n
        data = pix.samples  # byte array length w*h*n
        # decide sampling step so we take ~sample_count pixels
        step_pixels = max(1, (w * h) // sample_count)
        step_bytes  = step_pixels * n
        is_color = False
        for idx in range(0, len(data), step_bytes):
            if n >= 3:
                r, g, b = data[idx], data[idx+1], data[idx+2]
                if r != g or g != b:
                    is_color = True
                    break
        if is_color:
            color_pages.append(i)
    return color_pages

def split_pdf_by_color(input_pdf, n, cover_out, color_out, bw_out):
    src = fitz.open(input_pdf)
    total = src.page_count

    # 1) extract cover/front-matter
    cover = fitz.open()
    for i in range(min(n, total)):
        cover.insert_pdf(src, from_page=i, to_page=i)
    cover.save(cover_out)
    print(f"Saved cover/front-matter pages (1–{n}) → {cover_out}")

    # 2) detect color pages after page n
    color_list = detect_color_pages(src, start=n)
    color_set = set(color_list)

    # for two-sided printing: include the “partner” page
    for p in color_list:
        if ((p - n) % 2) == 0:
            partner = p + 1
        else:
            partner = p - 1
        if n <= partner < total:
            color_set.add(partner)

    # 3) split remaining pages into color vs BW
    color_pdf = fitz.open()
    bw_pdf    = fitz.open()
    for i in range(n, total):
        if i in color_set:
            color_pdf.insert_pdf(src, from_page=i, to_page=i)
        else:
            bw_pdf.insert_pdf(src, from_page=i, to_page=i)

    color_pdf.save(color_out)
    print(f"Saved color pages (+ partners) → {color_out}")

    bw_pdf.save(bw_out)
    print(f"Saved BW pages → {bw_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split a PDF into cover, color pages (with two-sided partners), and BW pages."
    )
    parser.add_argument("input_pdf", help="Path to the input PDF (from Word)")
    parser.add_argument(
        "-n", "--cover-pages", type=int, default=15,
        help="Number of front-matter pages to extract (cover, TOC, etc.)"
    )
    parser.add_argument(
        "--cover-out", default="cover_toc.pdf",
        help="Output filename for the first n pages"
    )
    parser.add_argument(
        "--color-out", default="color_pages.pdf",
        help="Output filename for color pages"
    )
    parser.add_argument(
        "--bw-out", default="bw_pages.pdf",
        help="Output filename for BW pages"
    )
    args = parser.parse_args()

    split_pdf_by_color(
        args.input_pdf,
        args.cover_pages,
        args.cover_out,
        args.color_out,
        args.bw_out
    )
