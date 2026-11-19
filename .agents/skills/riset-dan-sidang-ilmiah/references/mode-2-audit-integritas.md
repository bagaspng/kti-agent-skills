# Mode 2: Audit Integritas 7-Mode, *Claim-Faithfulness*, & Konsistensi Temporal

*(Adaptasi dari `academic-pipeline` Gate 2.5/4.5, Protokol L3 Zhao et al., & 5-Pass Temporal Verifier pada Academic Research Skills)*

Berkas rujukan ini digunakan untuk mengaudit naskah ilmiah secara ketat sebelum masuk ke tahap sidang/review maupun sebelum finalisasi akhir.

---

## 1. Daftar Periksa Kegagalan Riset AI 7-Mode (*7-Mode AI Failure Checklist*)

Berdasarkan taksonomi kegagalan sistem riset otonom (Lu et al., *Nature* 2026), setiap naskah wajib diperiksa terhadap 7 mode cacat berikut. Berikan status **`LULUS (CLEAR)`**, **`DICURIGAI (SUSPECTED)`**, atau **`GAGAL (FAIL)`** beserta lokasi paragraf/babnya:

| Kode | Mode Kegagalan | Apa yang Diperiksa di Naskah |
| :--- | :--- | :--- |
| **M1** | **Inkonsistensi Teknis / Implementasi** | Apakah ada kontradiksi antara spesifikasi sistem/rumus/diagram di satu bab dengan penjelasan di bab lain (misal: jumlah aktor, daftar endpoint, skema tabel, atau alur status berbeda antarbab)? |
| **M2** | **Sitasi Halusinasi (*Hallucinated Citation*)** | Apakah ada rujukan di dalam teks atau Daftar Pustaka yang tidak dapat ditemukan di Semantic Scholar, OpenAlex, Crossref, atau arXiv (dicek via `scripts/verifikasi_4indeks.py`)? |
| **M3** | **Angka / Hasil Tanpa Sumber (*Unanchored Result*)** | Apakah ada klaim angka, persentase, waktu respons, atau fakta lapangan yang muncul tiba-tiba tanpa rujukan atau tanpa berasal dari data eksperimen peneliti? |
| **M4** | **Penyederhanaan Berlebih (*Shortcut Reliance*)** | Apakah metodologi atau skenario pengujian yang dirancang terlalu dangkal untuk menjawab rumusan masalah yang diklaim di Bab I? |
| **M5** | **Keterbatasan yang Dipoles Jadi Keunggulan (*Bug-as-Insight*)** | Apakah ada keterbatasan/kekurangan desain yang dibungkus dengan kalimat retoris seolah-olah merupakan kontribusi ilmiah baru tanpa justifikasi literatur? |
| **M6** | **Fabrikasi Metodologi (*Methodology Fabrication*)** | Apakah tahapan metode (misal: tahapan Scrum, teknik *sampling*, atau prosedur pengujian) ditulis menggunakan istilah yang tidak sesuai dengan standar buku/pedoman resminya? |
| **M7** | **Kunci Kerangka (*Frame-Lock*)** | Apakah naskah hanya membandingkan solusi yang diusulkan dengan alternatif yang jelas-jelas lemah (*strawman*), tanpa membahas alternatif yang setara beserta *trade-off* jujurnya? |

---

## 2. Audit Kejujuran Klaim-Sitasi (*L3 Claim-Faithfulness*) & Anti-Leakage

Banyak naskah mengutip artikel yang nyata (DOI valid), namun **isi artikel tersebut sebenarnya tidak mendukung kalimat yang diklaim penulis** (fenomena *L3 Claim-Source Misalignment*, Zhao et al., 2026).

1. **Klasifikasi Status Klaim**:
   - **`SUPPORTED`**: Kalimat klaim sesuai dengan topik, ruang lingkup, dan temuan pada rujukan yang disitir.
   - **`OVERSTATED` (Klaim Berlebihan)**: Rujukan hanya menunjukkan korelasi atau studi kasus terbatas, tetapi naskah menulisnya sebagai bukti mutlak/universal (*"membuktikan bahwa selalu..."*).
   - **`MISMATCH` (Salah Tempel Sitasi)**: Judul/abstrak rujukan `[n]` membahas topik yang berbeda dari klaim di kalimat tersebut.
   - **`[MATERIAL GAP]` (Anti-Leakage Tag)**: Kalimat membuat klaim faktual/teknis spesifik (angka, standar hukum, perbandingan performa) tetapi **tidak memiliki sitasi sama sekali**. Jangan mengarang sitasi untuk menutupnya; tandai dengan `[MATERIAL GAP: butuh rujukan/data untuk ...]`.

---

## 3. Pemeriksa Konsistensi Waktu 5-Lapis (*5-Pass Temporal Verifier*)

Periksa lima jenis anomali waktu di seluruh naskah:
- **P1 (Aritmatika Durasi)**: Apakah durasi penelitian di narasi (misal: *"lima bulan, November 2026 – Maret 2027"*) cocok dengan jumlah kolom bulan di tabel jadwal dan jumlah siklus sprint/tahapan?
- **P2 (Anakronisme Rujukan)**: Apakah ada kutipan yang melanggar urutan waktu (misal: menulis *"Penelitian A (2021) mengembangkan lebih lanjut temuan Penelitian B (2024)"*)?
- **P3 (Pembanding Waktu)**: Apakah tabel perbandingan penelitian terdahulu sudah diurutkan secara logis dan konsisten tahun terbitnya?
- **P4 (Klaim Sebab-Akibat Lintas Waktu)**: Apakah regulasi/standar yang dikutip masih berlaku dan sesuai tahun terbitnya?
- **P5 (Deiksis Waktu / Klaim "Terbaru" yang Usang)**: Apakah naskah menyebut kata *"baru-baru ini"*, *"terkini"*, atau *"modern"* tetapi merujuk pada pustaka yang terbit lebih dari 8–10 tahun lalu?
