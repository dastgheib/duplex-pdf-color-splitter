# PDF Color Splitter

[![PyPI version](https://img.shields.io/pypi/v/PyMuPDF.svg)](https://pypi.org/project/PyMuPDF/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python script to split a PDF into:

* **Cover/Front‑Matter** pages (e.g., cover, table of contents)
* **Color** pages (plus their two‑sided printing partners)
* **Black & White** pages

This is useful for optimizing duplex printing by segregating color‑heavy content (figures, table headers) from purely black‑and‑white pages.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features

* Extract the first **N** pages (cover, TOC, etc.) into a separate PDF.
* Detect pages containing color content by sampling rendered pixels (default: ~1000 evenly spaced samples per page). Increase the sample_count parameter in the script to sample more pixels for finer-grained detection.
* Include two‑sided partners for each color page to avoid blank backs/forefronts when duplex printing.
* Separate the remaining pages into a BW‑only PDF.
* CLI interface with configurable parameters.

## Requirements

* Python 3.6+
* [PyMuPDF](https://pypi.org/project/PyMuPDF/)

Install dependencies with:

```bash
pip install pymupdf
```

## Installation

1. **Clone the repository**:

   ```bash
   ```

git clone [https://github.com/](https://github.com/)<your-username>/pdf-color-splitter.git
cd pdf-color-splitter

````

2. **Install dependencies**:

   ```bash
pip install -r requirements.txt
````

or directly:

```bash
pip install pymupdf
```

## Usage

Run the script with:

```bash
python split_pdf_by_color.py <input.pdf> \
  -n <cover_pages> \
  --cover-out <cover_toc.pdf> \
  --color-out <color_pages.pdf> \
  --bw-out <bw_pages.pdf>
```

### Arguments

* `<input.pdf>`: Path to the PDF generated from Word.
* `-n, --cover-pages`: Number of front‑matter pages to extract (default: `5`).
* `--cover-out`: Output filename for the cover/front-matter PDF (default: `cover_toc.pdf`).
* `--color-out`: Output filename for the color pages PDF (default: `color_pages.pdf`).
* `--bw-out`: Output filename for the BW pages PDF (default: `bw_pages.pdf`).

### Example

Extract the first **3** pages as cover and split `report.pdf`:

```bash
python split_pdf_by_color.py report.pdf -n 3
```

This produces:

* `cover_toc.pdf` (pages 1–3)
* `color_pages.pdf` (detected color pages + partners)
* `bw_pages.pdf` (remaining BW pages)

## Configuration

* **Sampling Density**: Modify `sample_count` in `split_pdf_by_color.py` to adjust pixel sampling per page (higher values improve detection accuracy at the cost of performance).
* **Default Outputs**: Change default filenames or add new CLI flags as needed.

## Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/XYZ`)
3. Commit your changes (`git commit -m 'Add XYZ'`)
4. Push to the branch (`git push origin feature/XYZ`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
