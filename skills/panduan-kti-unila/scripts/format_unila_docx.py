#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pemformat dan penyinkron otomatis dokumen .docx sesuai Panduan KTI Unila 2020.

Menerapkan aturan tata letak fisik, tipografi, penomoran halaman ganda,
format judul tabel/gambar, cetak miring istilah asing, dan sinkronisasi
nomor halaman Daftar Isi/Tabel/Gambar via Microsoft Word COM.

Pemakaian:
    python scripts/format_unila_docx.py input.docx
    python scripts/format_unila_docx.py input.docx --output output.docx --auto-italic --sync-toc
    python scripts/format_unila_docx.py input.docx --bump-version --sync-toc
"""
import argparse
import os
import re
import shutil
import sys
from pathlib import Path

import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor

FOREIGN_TERMS = [
    "Computer Based Test", "Role-Based Access Control", "role-based access control",
    "Broken Object Level Authorization", "Broken Authentication",
    "Broken Object Property Level Authorization", "Unrestricted Resource Consumption",
    "Broken Function Level Authorization", "Security Misconfiguration",
    "equivalence partitioning", "boundary value analysis", "Equivalence Partitioning",
    "Boundary Value Analysis", "black box testing", "Black box testing", "Black Box Testing",
    "white box testing", "security testing", "Security testing", "Security Testing",
    "load testing", "Load testing", "Load Testing", "penetration testing",
    "regression testing", "acceptance testing", "modular monolith", "Modular monolith",
    "Modular Monolith", "Microservice Premium", "microservices", "microservice",
    "monolithic", "monolith", "temporary signed URL", "signed URL", "signature pad",
    "rate limiting", "Rate limiting", "virtual users", "Virtual users",
    "Use Case Diagram", "Use case diagram", "diagram use case", "Activity Diagram",
    "Sequence Diagram", "Entity Relationship Diagram", "Structure Diagrams",
    "Behavioral Diagrams", "Product Owner", "Scrum Master", "Product Backlog",
    "Sprint Backlog", "Sprint Planning", "Sprint Execution", "Sprint Review",
    "Sprint Retrospective", "Sprint Goal", "Product Goal", "Daily Scrum",
    "Daily Meeting", "Definition of Done", "collection runner", "stack trace",
    "reverse proxy", "client-server", "client–server", "e-assessment",
    "single page application", "Single Page Application", "bearer token", "Bearer token",
    "foreign key", "primary key", "mass assignment", "auto-grading", "autosave",
    "web server", "spreadsheet", "paperless", "throughput", "stateless",
    "framework", "backend", "frontend", "endpoint", "database", "offline", "online",
    "increment", "Increment", "backlog", "sprint", "Sprint", "policy", "Policy",
    "hash", "login", "logout", "upload", "mock data", "mock API", "wireframe",
    "over-fetching", "under-fetching", "bounded context", "eventual consistency",
    "context switching", "greenfield",
]

FOREIGN_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_/.-])("
    + "|".join(re.escape(t) for t in sorted(set(FOREIGN_TERMS), key=len, reverse=True))
    + r")(?![A-Za-z0-9_/.-])"
)


def set_run_font(run, name="Times New Roman", size_pt=12, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)
    rFonts.set(qn("w:eastAsia"), name)


def add_formatted_text(para, text, size_pt=12, base_bold=False, base_italic=False, auto_italic_foreign=True):
    if not text:
        return
    if base_italic or not auto_italic_foreign:
        r = para.add_run(text)
        set_run_font(r, size_pt=size_pt, bold=base_bold, italic=base_italic)
        return
    last_idx = 0
    for m in FOREIGN_PATTERN.finditer(text):
        if m.start() > last_idx:
            r = para.add_run(text[last_idx:m.start()])
            set_run_font(r, size_pt=size_pt, bold=base_bold, italic=False)
        r_it = para.add_run(m.group(0))
        set_run_font(r_it, size_pt=size_pt, bold=base_bold, italic=True)
        last_idx = m.end()
    if last_idx < len(text):
        r = para.add_run(text[last_idx:])
        set_run_font(r, size_pt=size_pt, bold=base_bold, italic=False)


def clear_hf(hf):
    for p in hf.paragraphs:
        p.text = ""
        for ch in list(p._element):
            if not ch.tag.endswith("pPr"):
                p._element.remove(ch)


def add_page_number_to_paragraph(p, align=WD_PARAGRAPH_ALIGNMENT.RIGHT):
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run()
    set_run_font(r, size_pt=12)
    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instr = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls("w"))
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    r._r.append(fld1)
    r._r.append(instr)
    r._r.append(fld2)
    r._r.append(fld3)


def close_open_word_doc(target_paths):
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        norm_targets = {os.path.abspath(p).lower() for p in target_paths if p}
        for d in list(word.Documents):
            if os.path.abspath(d.FullName).lower() in norm_targets:
                print(f"[INFO] Menutup dokumen yang sedang terbuka di Word: {d.FullName}")
                d.Close(False)
    except Exception:
        pass


def format_unila_document(input_path, output_path, auto_italic=False):
    doc = docx.Document(input_path)

    # 1. Setup Base Styles
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.space_after = Pt(0)
    normal_style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

    for h_name, align, sb, sa in [
        ("Heading 1", WD_PARAGRAPH_ALIGNMENT.CENTER, 85, 24),
        ("Heading 2", WD_PARAGRAPH_ALIGNMENT.LEFT, 12, 6),
        ("Heading 3", WD_PARAGRAPH_ALIGNMENT.LEFT, 12, 6),
    ]:
        if h_name in doc.styles:
            st = doc.styles[h_name]
            st.font.name = "Times New Roman"
            st.font.size = Pt(12)
            st.font.bold = True
            st.font.color.rgb = RGBColor(0, 0, 0)
            st.paragraph_format.alignment = align
            st.paragraph_format.line_spacing = 1.0
            st.paragraph_format.space_before = Pt(sb)
            st.paragraph_format.space_after = Pt(sa)
            st.paragraph_format.keep_with_next = True

    # 2. Configure Margins (A4, Left 4cm, Top/Right/Bottom 3cm)
    for s in doc.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.left_margin = Cm(4.0)
        s.top_margin = Cm(3.0)
        s.right_margin = Cm(3.0)
        s.bottom_margin = Cm(3.0)
        s.header_distance = Cm(1.5)
        s.footer_distance = Cm(1.5)

    # 3. Configure Page Numbering if multi-section Unila layout
    if len(doc.sections) >= 3:
        s0 = doc.sections[0]
        s0.different_first_page_header_footer = True
        clear_hf(s0.header)
        clear_hf(s0.footer)
        clear_hf(s0.first_page_header)
        clear_hf(s0.first_page_footer)

        s1 = doc.sections[1]
        s1.header.is_linked_to_previous = False
        clear_hf(s1.header)
        s1.footer.is_linked_to_previous = False
        add_page_number_to_paragraph(s1.footer.paragraphs[0], WD_PARAGRAPH_ALIGNMENT.RIGHT)
        sectPr1 = s1._sectPr
        pgNumType1 = sectPr1.find(qn("w:pgNumType"))
        if pgNumType1 is None:
            pgNumType1 = parse_xml(r'<w:pgNumType %s w:fmt="lowerRoman" w:start="1"/>' % nsdecls("w"))
            sectPr1.append(pgNumType1)
        else:
            pgNumType1.set(qn("w:fmt"), "lowerRoman")
            pgNumType1.set(qn("w:start"), "1")

        # Determine first chapter section index (2 or 3 depending on continuous break)
        ch1_idx = 2
        if len(doc.sections) > 3 and doc.sections[2].start_type == 0:
            doc.sections[2].header.is_linked_to_previous = True
            doc.sections[2].footer.is_linked_to_previous = True
            ch1_idx = 3

        s_ch1 = doc.sections[ch1_idx]
        s_ch1.different_first_page_header_footer = True
        s_ch1.header.is_linked_to_previous = False
        add_page_number_to_paragraph(s_ch1.header.paragraphs[0], WD_PARAGRAPH_ALIGNMENT.RIGHT)
        s_ch1.footer.is_linked_to_previous = False
        clear_hf(s_ch1.footer)
        clear_hf(s_ch1.first_page_header)
        clear_hf(s_ch1.first_page_footer)
        sectPr_ch1 = s_ch1._sectPr
        pgNumType_ch1 = sectPr_ch1.find(qn("w:pgNumType"))
        if pgNumType_ch1 is None:
            pgNumType_ch1 = parse_xml(r'<w:pgNumType %s w:fmt="decimal" w:start="1"/>' % nsdecls("w"))
            sectPr_ch1.append(pgNumType_ch1)
        else:
            pgNumType_ch1.set(qn("w:fmt"), "decimal")
            pgNumType_ch1.set(qn("w:start"), "1")

        for idx in range(ch1_idx + 1, len(doc.sections)):
            s = doc.sections[idx]
            s.different_first_page_header_footer = True
            s.header.is_linked_to_previous = True
            s.footer.is_linked_to_previous = True
            clear_hf(s.first_page_header)
            clear_hf(s.first_page_footer)
            sectPr = s._sectPr
            pgNumType = sectPr.find(qn("w:pgNumType"))
            if pgNumType is not None:
                if qn("w:start") in pgNumType.attrib:
                    del pgNumType.attrib[qn("w:start")]
                pgNumType.set(qn("w:fmt"), "decimal")

    # 4. Process Paragraphs
    in_cover = True
    in_abstract = False
    in_front_list = False
    in_daftar_pustaka = False

    for p in doc.paragraphs:
        text = p.text.strip()
        style_name = p.style.name if p.style else "Normal"

        if style_name == "Heading 1" and text.upper() in ("ABSTRAK", "ABSTRACT", "KATA PENGANTAR", "PRAKATA"):
            in_cover = False
            in_abstract = text.upper() in ("ABSTRAK", "ABSTRACT")
            in_front_list = False
        elif style_name == "Heading 1" and text.upper() in ("DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR", "DAFTAR LAMPIRAN"):
            in_cover = False
            in_abstract = False
            in_front_list = True
        elif style_name == "Heading 1" and (text.upper().startswith("BAB ") or text.upper().startswith("I.")):
            in_cover = False
            in_abstract = False
            in_front_list = False
        elif style_name == "Heading 1" and "DAFTAR PUSTAKA" in text.upper():
            in_cover = False
            in_abstract = False
            in_front_list = False
            in_daftar_pustaka = True

        if style_name == "Heading 1":
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(85)
            p.paragraph_format.space_after = Pt(24)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                set_run_font(r, size_pt=12, bold=True, italic=bool(r.italic))
            continue

        if style_name in ("Heading 2", "Heading 3"):
            p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            if p.text.rstrip().endswith("."):
                p.text = p.text.rstrip().rstrip(".")
            for r in p.runs:
                set_run_font(r, size_pt=12, bold=True, italic=bool(r.italic))
            continue

        # Table Captions (Tabel X.Y ...) -> Left, no trailing period
        if re.match(r"^Tabel\s+\d+\.\d+\b", text) and len(text) < 250 and "\t" not in text:
            p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.first_line_indent = Pt(0)
            p.paragraph_format.keep_with_next = True
            for r in reversed(p.runs):
                if r.text.strip():
                    if r.text.rstrip().endswith("."):
                        r.text = r.text.rstrip().rstrip(".")
                    break
            for r in p.runs:
                set_run_font(r, size_pt=12, bold=bool(r.bold), italic=bool(r.italic))
            continue

        # Figure Captions (Gambar X.Y ...) -> Center, must end with period
        if re.match(r"^Gambar\s+\d+\.\d+\.?\b", text) and len(text) < 250 and "\t" not in text:
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(18)
            p.paragraph_format.first_line_indent = Pt(0)
            for r in reversed(p.runs):
                if r.text.strip():
                    if not r.text.rstrip().endswith("."):
                        r.text = r.text.rstrip() + "."
                    break
            for r in p.runs:
                set_run_font(r, size_pt=12, bold=bool(r.bold), italic=bool(r.italic))
            continue

        if in_cover or in_abstract or in_front_list or in_daftar_pustaka:
            for r in p.runs:
                set_run_font(r, size_pt=12, bold=bool(r.bold), italic=bool(r.italic))
            continue

        # Narrative body paragraphs
        if text:
            if auto_italic:
                # Re-split non-italic runs containing FOREIGN_TERMS
                old_runs = [(r.text, bool(r.bold), bool(r.italic)) for r in p.runs if r.text]
                if any(not it and FOREIGN_PATTERN.search(t) for t, _, it in old_runs):
                    p.text = ""
                    for t, b, it in old_runs:
                        add_formatted_text(p, t, size_pt=12, base_bold=b, base_italic=it, auto_italic_foreign=True)
            for r in p.runs:
                set_run_font(r, size_pt=12, bold=bool(r.bold), italic=bool(r.italic))

    # 5. Format Tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.0
                    p.paragraph_format.first_line_indent = Pt(0)
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        if r.font.size is None or r.font.size.pt > 11:
                            r.font.size = Pt(11)

    doc.save(output_path)
    print(f"[OK] Dokumen berhasil diformat sesuai Panduan Unila 2020: {output_path}")


def sync_word_toc_and_lists(docx_path):
    try:
        import win32com.client
    except ImportError:
        print("[WARN] pywin32 tidak tersedia; lewati sinkronisasi otomatis Word COM.", file=sys.stderr)
        return

    abs_path = os.path.abspath(docx_path)
    word = win32com.client.Dispatch("Word.Application")
    wdoc = word.Documents.Open(abs_path)
    try:
        wdoc.Repaginate()
        for fld in wdoc.Fields:
            fld.Update()
        for toc in wdoc.TablesOfContents:
            toc.Update()
        wdoc.Repaginate()

        caption_pages = {}
        for p in wdoc.Paragraphs:
            txt = p.Range.Text.strip()
            if (re.match(r"^(Tabel|Gambar)\s+\d+\.\d+", txt) and "\t" not in txt and len(txt) < 250):
                pg = p.Range.Information(1)  # wdActiveEndAdjustedPageNumber
                caption_pages[txt] = str(pg)

        wdoc.Save()
    finally:
        wdoc.Close(False)

    if caption_pages:
        pdoc = docx.Document(abs_path)
        updated = 0
        for p in pdoc.paragraphs:
            t = p.text.strip()
            if "\t" not in t:
                continue
            for cap, pg in caption_pages.items():
                parts = cap.split(" ", 2)
                if len(parts) < 3:
                    continue
                num_part = parts[1].rstrip(".")
                title_part = parts[2].rstrip(".")
                if t.startswith(num_part) and title_part[:25] in t:
                    head, sep, old_pg = p.text.rpartition("\t")
                    if sep and old_pg.strip() != pg:
                        p.text = ""
                        add_formatted_text(p, f"{head}\t{pg}", size_pt=12, base_bold=False, auto_italic_foreign=True)
                        updated += 1
                    break
        if updated:
            pdoc.save(abs_path)
            wdoc = word.Documents.Open(abs_path)
            try:
                wdoc.Repaginate()
                for toc in wdoc.TablesOfContents:
                    toc.Update()
                wdoc.Save()
            finally:
                wdoc.Close(False)
        print(f"[OK] Sinkronisasi Daftar Isi, Daftar Tabel, dan Daftar Gambar selesai ({updated} item diperbarui).")


def resolve_bump_version(input_path, backup_dir=None):
    p = Path(input_path).resolve()
    m = re.match(r"^(.*?(?:_p|_v|p))(\d+)(\.docx)$", p.name, re.I)
    if not m:
        return str(p), None
    prefix, num_str, ext = m.groups()
    next_num = int(num_str) + 1
    out_path = p.parent / f"{prefix}{next_num}{ext}"
    b_dir = Path(backup_dir) if backup_dir else (p.parent / "backup")
    b_dir.mkdir(parents=True, exist_ok=True)
    b_path = b_dir / p.name
    return str(out_path), str(b_path)


def main():
    parser = argparse.ArgumentParser(description="Format & Sinkronisasi DOCX sesuai Panduan KTI Unila 2020")
    parser.add_argument("input", help="Path berkas .docx masukan")
    parser.add_argument("--output", "-o", help="Path berkas .docx keluaran (opsional)")
    parser.add_argument("--bump-version", action="store_true", help="Naikkan nomor versi (pN -> pN+1) dan pindahkan versi lama ke backup/")
    parser.add_argument("--backup-dir", help="Direktori arsip backup (default: ./backup)")
    parser.add_argument("--auto-italic", action="store_true", help="Otomatis cetak miring istilah asing (FOREIGN_TERMS)")
    parser.add_argument("--sync-toc", action="store_true", help="Sinkronkan nomor halaman Daftar Isi/Tabel/Gambar via Word COM")
    args = parser.parse_args()

    in_path = os.path.abspath(args.input)
    if not os.path.exists(in_path):
        print(f"[ERROR] Berkas tidak ditemukan: {in_path}", file=sys.stderr)
        return 1

    backup_dest = None
    if args.bump_version:
        out_path, backup_dest = resolve_bump_version(in_path, args.backup_dir)
    else:
        out_path = os.path.abspath(args.output) if args.output else in_path

    close_open_word_doc([in_path, out_path])

    if backup_dest and os.path.abspath(in_path) != os.path.abspath(out_path):
        shutil.copy2(in_path, backup_dest)
        print(f"[INFO] Mengarsipkan versi sebelumnya ke: {backup_dest}")

    format_unila_document(in_path, out_path, auto_italic=args.auto_italic)

    if args.sync_toc:
        sync_word_toc_and_lists(out_path)

    if args.bump_version and backup_dest and os.path.abspath(in_path) != os.path.abspath(out_path):
        try:
            os.remove(in_path)
            print(f"[INFO] Berkas lama di root dipindahkan ke backup: {os.path.basename(in_path)}")
        except Exception as e:
            print(f"[WARN] Gagal menghapus berkas lama {in_path}: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
