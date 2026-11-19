#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditor Klaim-Sitasi (L3 Claim-Faithfulness), Anti-Leakage [MATERIAL GAP], & Konsistensi Temporal.

Adaptasi dari Gate 2.5/4.5, L3 Claim-Faithfulness Audit, dan 5-Pass Temporal Verifier
pada Academic Research Skills (ARS) untuk berkas .docx maupun .md.

Pemakaian:
    python scripts/audit_klaim_docx.py naskah.docx [--output laporan_audit_klaim.md]
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

CITE_IEEE_RX = re.compile(r"\[(\d+(?:\s*[-–,]\s*\d+)*)\]")
YEAR_IN_TEXT_RX = re.compile(r"\b(19\d{2}|20[0-2]\d)\b")
RECENT_WORDS_RX = re.compile(r"\b(baru-baru ini|terbaru|terkini|mutakhir|beberapa tahun terakhir|dewasa ini)\b", re.I)
STRONG_CLAIM_RX = re.compile(
    r"\b(\d+(?:[.,]\d+)?\s*(?:%|ms|detik|req/s|rps|kali lipat)|membuktikan bahwa|secara signifikan|menurut standar|berdasarkan peraturan)\b",
    re.I
)
DURATION_RX = re.compile(
    r"\b(?:selama\s+)?(tiga|empat|lima|enam|tujuh|delapan|\d+)\s+bulan\b",
    re.I
)


def read_paragraphs(file_path):
    p = Path(file_path)
    if p.suffix.lower() == ".docx":
        with zipfile.ZipFile(p) as z, z.open("word/document.xml") as f:
            root = ET.parse(f).getroot()
        paras = []
        for idx, el in enumerate((e for e in root.iter() if e.tag.endswith(("}p", ":p")) or e.tag == "p"), 1):
            txt = "".join(t.text or "" for t in el.iter() if t.tag.endswith(("}t", ":t")) or t.tag == "t").strip()
            if txt:
                paras.append((idx, txt))
        return paras
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    return [(i, l.strip()) for i, l in enumerate(lines, 1) if l.strip()]


def expand_ieee_nums(cite_str):
    nums = []
    for part in re.split(r"\s*,\s*", cite_str):
        rng = re.split(r"\s*[-–]\s*", part)
        if len(rng) == 2 and rng[0].isdigit() and rng[1].isdigit():
            nums.extend(range(int(rng[0]), int(rng[1]) + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums


def audit_document(file_path):
    paras = read_paragraphs(file_path)
    in_body = False
    in_pustaka = False
    current_section = "Bagian Awal"

    bib_map = {}
    claim_pairs = []
    material_gaps = []
    temporal_warnings = []
    durations_found = []

    # Pass 1: Kumpulkan Daftar Pustaka terlebih dahulu
    temp_pustaka = False
    for idx, txt in paras:
        upper = txt.upper()
        if "DAFTAR PUSTAKA" in upper and len(txt) < 40:
            temp_pustaka = True
            continue
        if temp_pustaka:
            m_bib = re.match(r"^\[(\d+)\]\s*(.+)$", txt)
            if m_bib:
                bib_map[int(m_bib.group(1))] = m_bib.group(2).strip()

    # Pass 2: Analisis Batang Tubuh
    for idx, txt in paras:
        upper = txt.upper()
        if re.match(r"^(?:BAB\s+[IVX]+|[IVX]+\.\s+PENDAHULUAN)", upper) and "\t" not in txt:
            in_body = True
            in_pustaka = False
            current_section = txt[:60]
            continue
        if "DAFTAR PUSTAKA" in upper and len(txt) < 40:
            in_body = False
            in_pustaka = True
            current_section = "DAFTAR PUSTAKA"
            continue
        if not in_body or in_pustaka:
            continue

        if re.match(r"^\d+\.\d+(?:\.\d+)?\s+[A-Z]", txt) and len(txt) < 120 and "\t" not in txt:
            current_section = txt
            continue

        # Cek pernyataan durasi (Temporal P1)
        for dm in DURATION_RX.finditer(txt):
            durations_found.append((idx, current_section, dm.group(0), txt[:140]))

        # Pecah per kalimat
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", txt)
        for sent in sentences:
            s_clean = " ".join(sent.split())
            if len(s_clean) < 25:
                continue
            cites = CITE_IEEE_RX.findall(s_clean)
            if cites:
                cited_ids = []
                for c in cites:
                    cited_ids.extend(expand_ieee_nums(c))
                refs = [f"[{n}] {bib_map.get(n, '(Tidak ditemukan di Daftar Pustaka!)')}" for n in sorted(set(cited_ids))]
                claim_pairs.append({
                    "para": idx,
                    "section": current_section,
                    "claim_sentence": s_clean,
                    "cited_refs": refs,
                })
                # Cek Temporal P5: kata "terbaru/baru-baru ini" tapi merujuk tahun tua (< 2018)
                if RECENT_WORDS_RX.search(s_clean):
                    for n in set(cited_ids):
                        ref_txt = bib_map.get(n, "")
                        yrs = [int(y) for y in YEAR_IN_TEXT_RX.findall(ref_txt) if 1980 <= int(y) <= 2027]
                        if yrs and max(yrs) < 2018:
                            temporal_warnings.append((
                                idx, current_section,
                                f"Klaim menyebut '{RECENT_WORDS_RX.search(s_clean).group(0)}' tetapi merujuk [{n}] bertahun {max(yrs)}",
                                s_clean[:140]
                            ))
            else:
                # Cek Anti-Leakage [MATERIAL GAP]: klaim kuantitatif/standar di Bab I/II tanpa sitasi
                if ("BAB I" in current_section.upper() or "BAB II" in current_section.upper() or current_section.startswith(("1.", "2."))):
                    if STRONG_CLAIM_RX.search(s_clean) and not re.search(r"\b(penelitian ini|batasan|rumusan|tujuan|tabel|gambar)\b", s_clean, re.I):
                        material_gaps.append((idx, current_section, STRONG_CLAIM_RX.search(s_clean).group(0), s_clean))

    # Cek konsistensi durasi bulan antar-bagian (Temporal P1)
    distinct_durations = {d[2].lower() for d in durations_found}
    if len(distinct_durations) > 1:
        temporal_warnings.append((
            durations_found[0][0], "Lintas-Bab (Temporal P1)",
            f"Ditemukan penyebutan durasi bulan yang berbeda antarbab: {sorted(distinct_durations)}",
            " | ".join(f"P{d[0]} ({d[1]}): {d[2]}" for d in durations_found)
        ))

    return {
        "total_bib": len(bib_map),
        "total_claim_sentences": len(claim_pairs),
        "material_gaps": material_gaps,
        "temporal_warnings": temporal_warnings,
        "durations": durations_found,
        "claim_pairs": claim_pairs,
    }


def render_report(file_path, data):
    out = [
        f"# Laporan Audit Klaim-Sitasi (L3) & Konsistensi Temporal",
        f"- **Berkas**: `{file_path}`",
        f"- **Total Entri Daftar Pustaka**: {data['total_bib']}",
        f"- **Total Kalimat Klaim Bersitasi**: {data['total_claim_sentences']}",
        f"- **Potensi `[MATERIAL GAP]` (Klaim Kuat Tanpa Sitasi di Bab I/II)**: {len(data['material_gaps'])}",
        f"- **Peringatan Konsistensi Temporal (5-Pass)**: {len(data['temporal_warnings'])}",
        "",
        "---",
        "",
        "## 1. Pemeriksaan Konsistensi Temporal (P1–P5)",
    ]
    if data["temporal_warnings"]:
        for p_idx, sec, msg, snip in data["temporal_warnings"]:
            out.append(f"- **Paragraf {p_idx} ({sec})**: {msg}\n  > *{snip}*")
    else:
        out.append("- `[LULUS]` Tidak ditemukan kontradiksi durasi waktu atau anakronisme sitasi.")

    out.extend(["", "## 2. Deteksi Anti-Leakage (`[MATERIAL GAP]` Kandidat)"])
    if data["material_gaps"]:
        for p_idx, sec, trig, sent in data["material_gaps"][:20]:
            out.append(f"- **Paragraf {p_idx} ({sec})** — Pemicu `{trig}` tanpa sitasi:\n  > {sent}")
    else:
        out.append("- `[LULUS]` Tidak ditemukan klaim angka/standar tanpa sitasi pada Bab I–II.")

    out.extend([
        "",
        "## 3. Peta Pasangan Klaim ↔ Rujukan (Untuk Audit *L3 Claim-Faithfulness*)",
        "Periksa apakah isi rujukan di bawah benar-benar mendukung klaim kalimatnya:",
        "",
    ])
    for item in data["claim_pairs"][:50]:
        out.append(f"### Paragraf {item['para']} ({item['section']})")
        out.append(f"- **Kalimat Klaim**: {item['claim_sentence']}")
        for r in item["cited_refs"]:
            out.append(f"  - **Rujukan**: `{r}`")
        out.append("")

    return "\n".join(out)


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Audit pasangan klaim-sitasi (L3), [MATERIAL GAP], dan konsistensi waktu")
    parser.add_argument("input", help="Path berkas .docx atau .md")
    parser.add_argument("--output", "-o", help="Simpan laporan hasil audit ke berkas .md")
    args = parser.parse_args()

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        print(f"[ERROR] Berkas tidak ditemukan: {in_path}", file=sys.stderr)
        return 1

    data = audit_document(in_path)
    report = render_report(in_path.name, data)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"[OK] Laporan audit klaim disimpan ke: {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
