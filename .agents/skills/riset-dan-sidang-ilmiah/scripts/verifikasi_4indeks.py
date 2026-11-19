#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifikator sitasi deterministik 4-Indeks (Semantic Scholar + OpenAlex + Crossref + arXiv).

Adaptasi dari Four-Index Triangulation Gate (v3.11) pada Academic Research Skills (ARS).
Memeriksa keberadaan artikel ilmiah secara silang di 4 database akademik publik
menggunakan Python standard library (tanpa dependensi eksternal).

Pemakaian:
    python scripts/verifikasi_4indeks.py --judul "Judul Artikel" [--doi 10.xxx/yyy] [--tahun 2024]
    python scripts/verifikasi_4indeks.py --doi 10.1109/ACCESS.2022.3168684
"""
import argparse
import difflib
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HEADERS = {"User-Agent": "ARS-Unila-Verifier/1.0 (mailto:academic-verifier@example.edu)"}


def norm_title(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"[^\w\s]", " ", s.lower())
    return " ".join(s.split())


def title_sim(a, b):
    na, nb = norm_title(a), norm_title(b)
    if not na or not nb:
        return 0.0
    return round(difflib.SequenceMatcher(None, na, nb).ratio(), 3)


def http_get_json(url, timeout=10):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def check_openalex(title=None, doi=None):
    try:
        if doi:
            clean_doi = doi.strip().replace("https://doi.org/", "")
            url = f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(clean_doi)}"
            data = http_get_json(url)
            found_title = data.get("title") or ""
            sim = title_sim(title, found_title) if title else 1.0
            return {
                "matched": sim >= 0.70,
                "title": found_title,
                "year": data.get("publication_year"),
                "doi": data.get("doi"),
                "similarity": sim,
            }
        if title:
            q = urllib.parse.quote(title)
            url = f"https://api.openalex.org/works?search={q}&per-page=3"
            data = http_get_json(url)
            best, best_sim = None, 0.0
            for item in data.get("results", []):
                t = item.get("title") or ""
                s = title_sim(title, t)
                if s > best_sim:
                    best, best_sim = item, s
            if best:
                return {
                    "matched": best_sim >= 0.70,
                    "title": best.get("title"),
                    "year": best.get("publication_year"),
                    "doi": best.get("doi"),
                    "similarity": best_sim,
                }
    except Exception as e:
        return {"matched": False, "error": str(e)}
    return {"matched": False}


def check_crossref(title=None, doi=None):
    try:
        if doi:
            clean_doi = doi.strip().replace("https://doi.org/", "")
            url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
            data = http_get_json(url).get("message", {})
            titles = data.get("title") or [""]
            found_title = titles[0] if titles else ""
            sim = title_sim(title, found_title) if title else 1.0
            yr = None
            for k in ("published-print", "published-online", "issued"):
                parts = data.get(k, {}).get("date-parts", [[]])
                if parts and parts[0]:
                    yr = parts[0][0]
                    break
            return {
                "matched": sim >= 0.70,
                "title": found_title,
                "year": yr,
                "doi": data.get("DOI"),
                "similarity": sim,
            }
        if title:
            q = urllib.parse.quote(title)
            url = f"https://api.crossref.org/works?query.bibliographic={q}&rows=3"
            items = http_get_json(url).get("message", {}).get("items", [])
            best, best_sim = None, 0.0
            for it in items:
                t = (it.get("title") or [""])[0]
                s = title_sim(title, t)
                if s > best_sim:
                    best, best_sim = it, s
            if best:
                yr = None
                for k in ("published-print", "published-online", "issued"):
                    parts = best.get(k, {}).get("date-parts", [[]])
                    if parts and parts[0]:
                        yr = parts[0][0]
                        break
                return {
                    "matched": best_sim >= 0.70,
                    "title": (best.get("title") or [""])[0],
                    "year": yr,
                    "doi": best.get("DOI"),
                    "similarity": best_sim,
                }
    except Exception as e:
        return {"matched": False, "error": str(e)}
    return {"matched": False}


def check_semantic_scholar(title=None, doi=None):
    try:
        if doi:
            clean_doi = doi.strip().replace("https://doi.org/", "")
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(clean_doi)}?fields=title,year,externalIds"
            data = http_get_json(url)
            found_title = data.get("title") or ""
            sim = title_sim(title, found_title) if title else 1.0
            return {
                "matched": sim >= 0.70,
                "title": found_title,
                "year": data.get("year"),
                "doi": (data.get("externalIds") or {}).get("DOI"),
                "similarity": sim,
            }
        if title:
            q = urllib.parse.quote(title)
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}&limit=3&fields=title,year,externalIds"
            data = http_get_json(url)
            best, best_sim = None, 0.0
            for it in data.get("data", []):
                t = it.get("title") or ""
                s = title_sim(title, t)
                if s > best_sim:
                    best, best_sim = it, s
            if best:
                return {
                    "matched": best_sim >= 0.70,
                    "title": best.get("title"),
                    "year": best.get("year"),
                    "doi": (best.get("externalIds") or {}).get("DOI"),
                    "similarity": best_sim,
                }
    except Exception as e:
        return {"matched": False, "error": str(e)}
    return {"matched": False}


def check_arxiv(title=None):
    if not title:
        return {"matched": False}
    try:
        q = urllib.parse.quote(f'ti:"{title}"')
        url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=3"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_text = resp.read().decode("utf-8", errors="replace")
        root = ET.fromstring(xml_text)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        best_title, best_yr, best_id, best_sim = None, None, None, 0.0
        for entry in root.findall("a:entry", ns):
            t_el = entry.find("a:title", ns)
            p_el = entry.find("a:published", ns)
            id_el = entry.find("a:id", ns)
            t = " ".join((t_el.text or "").split()) if t_el is not None else ""
            s = title_sim(title, t)
            if s > best_sim:
                best_sim = s
                best_title = t
                best_yr = int(p_el.text[:4]) if (p_el is not None and p_el.text) else None
                best_id = id_el.text if id_el is not None else None
        if best_title:
            return {
                "matched": best_sim >= 0.70,
                "title": best_title,
                "year": best_yr,
                "arxiv_id": best_id,
                "similarity": best_sim,
            }
    except Exception as e:
        return {"matched": False, "error": str(e)}
    return {"matched": False}


def verify_reference(title=None, doi=None, year=None):
    results = {
        "OpenAlex": check_openalex(title, doi),
        "Crossref": check_crossref(title, doi),
        "SemanticScholar": check_semantic_scholar(title, doi),
        "arXiv": check_arxiv(title),
    }
    matched_indices = [k for k, v in results.items() if v.get("matched")]
    k_score = len(matched_indices)
    if k_score >= 3:
        status = f"TERVERIFIKASI KUAT ({k_score}/4 indeks cocok)"
    elif k_score >= 1:
        status = f"TERVERIFIKASI SEBAGIAN ({k_score}/4 indeks cocok: {', '.join(matched_indices)})"
    else:
        status = "TIDAK DITEMUKAN (0/4 indeks — periksa kemungkinan salah ketik atau halusinasi)"

    return {
        "query": {"title": title, "doi": doi, "year": year},
        "matched_count": k_score,
        "matched_indices": matched_indices,
        "status": status,
        "details": results,
    }


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Triangulasi sitasi ilmiah ke 4 indeks (OpenAlex, Crossref, Semantic Scholar, arXiv)")
    parser.add_argument("--judul", "-t", help="Judul artikel yang diperiksa")
    parser.add_argument("--doi", "-d", help="DOI artikel (opsional)")
    parser.add_argument("--tahun", "-y", type=int, help="Tahun terbit (opsional)")
    args = parser.parse_args()

    if not args.judul and not args.doi:
        parser.print_help()
        return 2

    res = verify_reference(title=args.judul, doi=args.doi, year=args.tahun)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res["matched_count"] >= 1 else 1


if __name__ == "__main__":
    sys.exit(main())
