#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pemindai korpus PDF jurnal lokal untuk ekstraksi matriks WHY / HOW / WHAT.

Adaptasi dari scripts/adapters/folder_scan.py pada Academic Research Skills (ARS).
Memindai seluruh berkas .pdf di dalam sebuah folder, mengekstrak DOI, tahun,
judul perkiraan, abstrak, serta cuplikan bagian Metode dan Hasil/Kesimpulan.

Pemakaian:
    python scripts/scan_korpus_pdf.py <folder_pdf> [--output hasil_korpus.md] [--json hasil.json]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DOI_RX = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b")
YEAR_RX = re.compile(r"\b(19\d{2}|20[0-2]\d)\b")


def extract_pdf_text(pdf_path, max_pages=15):
    """Ekstrak teks dari PDF menggunakan pypdf, fitz (PyMuPDF), atau pdftotext."""
    # 1. Coba pypdf / PyPDF2
    for mod_name in ("pypdf", "PyPDF2"):
        try:
            mod = __import__(mod_name)
            reader = mod.PdfReader(str(pdf_path))
            pages_text = []
            for idx, page in enumerate(reader.pages[:max_pages]):
                pages_text.append(page.extract_text() or "")
            return "\n".join(pages_text), len(reader.pages)
        except Exception:
            pass

    # 2. Coba PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        total = len(doc)
        pages_text = [doc[i].get_text("text") for i in range(min(total, max_pages))]
        doc.close()
        return "\n".join(pages_text), total
    except Exception:
        pass

    # 3. Coba pdftotext CLI
    try:
        res = subprocess.run(
            ["pdftotext", "-f", "1", "-l", str(max_pages), str(pdf_path), "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout, -1
    except Exception:
        pass

    return "", 0


def clean_whitespace(s):
    return " ".join((s or "").split())


def extract_section_snippet(text, headings, max_chars=700):
    for h in headings:
        pat = re.compile(rf"(?:^|\n)\s*(?:\d+\.?\s*|I+V?\.?\s*)?{h}\s*(?:\n|:)", re.I)
        m = pat.search(text)
        if m:
            snippet = text[m.end():m.end() + max_chars * 2]
            return clean_whitespace(snippet)[:max_chars]
    return ""


def parse_pdf_metadata(pdf_path):
    raw_text, num_pages = extract_pdf_text(pdf_path)
    lines = [clean_whitespace(l) for l in raw_text.splitlines() if len(clean_whitespace(l)) > 3]
    first_page_text = "\n".join(lines[:60])

    # Cari DOI
    doi_m = DOI_RX.search(raw_text[:6000])
    doi = doi_m.group(1).rstrip(".,;)") if doi_m else None

    # Cari Tahun
    years = [int(y) for y in YEAR_RX.findall(first_page_text) if 1990 <= int(y) <= 2027]
    year = max(set(years), key=years.count) if years else None

    # Perkiraan Judul (ambil baris non-header jurnal di awal dokumen)
    skip_rx = re.compile(r"(issn|volume|vol\.|no\.|journal|jurnal|available online|http|doi:|universitas|fakultas|procedia|ieee)", re.I)
    title_candidates = [l for l in lines[:15] if 15 <= len(l) <= 220 and not skip_rx.search(l)]
    title = title_candidates[0] if title_candidates else pdf_path.stem

    # Ekstrak Abstrak (WHY/HOW/WHAT ringkas)
    abstract = extract_section_snippet(
        raw_text,
        [r"abstrak", r"abstract", r"ringkasan"],
        max_chars=900
    )
    if not abstract and len(lines) > 3:
        abstract = clean_whitespace(" ".join(lines[2:18]))[:800]

    # Ekstrak cuplikan Metode (HOW) dan Hasil/Kesimpulan (WHAT)
    method_snip = extract_section_snippet(
        raw_text,
        [r"metode(?:\s+penelitian)?", r"metodologi(?:\s+penelitian)?", r"methodology", r"research\s+method(?:s)?", r"proposed\s+method"],
        max_chars=600
    )
    result_snip = extract_section_snippet(
        raw_text,
        [r"kesimpulan", r"simpulan", r"conclusion(?:s)?", r"hasil\s+dan\s+pembahasan", r"results?\s+and\s+discussion"],
        max_chars=600
    )

    return {
        "file_name": pdf_path.name,
        "file_path": str(pdf_path.resolve()),
        "pages": num_pages,
        "guessed_title": title,
        "year": year,
        "doi": doi,
        "abstract_snippet": abstract or "[Teks abstrak tidak terdeteksi otomatis]",
        "how_method_snippet": method_snip or "[Cuplikan metode perlu dibaca langsung]",
        "what_result_snippet": result_snip or "[Cuplikan hasil/kesimpulan perlu dibaca langsung]",
    }


def format_markdown_report(folder_path, items):
    out = [
        f"# Laporan Pemindaian Korpus PDF Lokal (`Corpus-First`)",
        f"- **Folder Sumber**: `{folder_path}`",
        f"- **Total Berkas PDF**: {len(items)}",
        "",
        "---",
        "",
    ]
    for idx, it in enumerate(items, 1):
        out.extend([
            f"## {idx}. `{it['file_name']}`",
            f"- **Perkiraan Judul**: {it['guessed_title']}",
            f"- **Tahun Terdeteksi**: {it['year'] or 'Tidak terdeteksi'} | **Halaman**: {it['pages'] or '?'} | **DOI**: `{it['doi'] or 'Tidak ada'}`",
            f"- **Abstrak / Konteks (WHY)**: {it['abstract_snippet']}",
            f"- **Cuplikan Metode (HOW)**: {it['how_method_snippet']}",
            f"- **Cuplikan Hasil/Simpulan (WHAT)**: {it['what_result_snippet']}",
            "",
        ])
    return "\n".join(out)


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Pindai folder PDF jurnal lokal untuk ekstraksi WHY/HOW/WHAT")
    parser.add_argument("folder", help="Path folder berisi berkas .pdf")
    parser.add_argument("--output", "-o", help="Simpan hasil laporan dalam format Markdown (.md)")
    parser.add_argument("--json", help="Simpan hasil laporan dalam format JSON (.json)")
    args = parser.parse_args()

    target_dir = Path(args.folder).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"[ERROR] Direktori tidak ditemukan: {target_dir}", file=sys.stderr)
        return 1

    pdf_files = sorted(target_dir.rglob("*.pdf"))
    if not pdf_files:
        print(f"[WARN] Tidak ada berkas .pdf di dalam: {target_dir}")
        return 0

    results = [parse_pdf_metadata(p) for p in pdf_files]
    md_report = format_markdown_report(target_dir, results)

    if args.output:
        Path(args.output).write_text(md_report, encoding="utf-8")
        print(f"[OK] Laporan Markdown disimpan ke: {args.output}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] Data JSON disimpan ke: {args.json}")
    if not args.output and not args.json:
        print(md_report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
