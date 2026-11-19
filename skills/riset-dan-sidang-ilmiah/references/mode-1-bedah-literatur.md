# Mode 1: Bedah Literatur, Korpus PDF Lokal, & Perumusan Masalah (`WHY / HOW / WHAT`)

*(Adaptasi dari `deep-research` & `folder_scan` pada Academic Research Skills — Cheng-I Wu)*

Berkas rujukan ini memandu proses pemetaan literatur ilmiah, pembedahan jurnal secara terstruktur, dan pembimbingan Socratic dalam merumuskan pertanyaan penelitian (*Research Question* / RQ) serta metodologi.

---

## 1. Prinsip *Corpus-First, Search-Fills-Gap* (4 Aturan Besi)

Ketika peneliti memiliki koleksi PDF jurnal lokal (atau daftar pustaka awal), agen wajib mendahulukan korpus milik peneliti sebelum mencari literatur tambahan di internet/API:

1. **Kriteria Seleksi Seragam (*Same Criteria*)**: Terapkan kriteria inklusi dan eksklusi yang sama ketatnya terhadap PDF lokal maupun hasil pencarian database eksternal.
2. **Tanpa Lewat Diam-Diam (*No Silent Skip*)**: Setiap jurnal di dalam folder peneliti yang tidak dimasukkan ke dalam matriks tinjauan pustaka wajib dicatat alasannya (misal: topik terlalu jauh, bukan artikel primer, atau tidak memuat evaluasi).
3. **Dilarang Mengarang Isi Korpus (*No Corpus Mutation*)**: Hanya gunakan fakta, metode, dataset, dan angka hasil yang benar-benar tertulis di dalam teks PDF/abstrak. Jika teks lengkap tidak terbaca atau terpotong, tandai bagian tersebut secara jujur sebagai `[BELUM TERVERIFIKASI DI TEKS LENGKAP]`.
4. **Penutupan Celah (*Search-Fills-Gap*)**: Setelah seluruh korpus lokal dipetakan, identifikasi sub-topik atau landasan metodologi yang belum memiliki rujukan, lalu cari rujukan pelengkap melalui `scripts/verifikasi_4indeks.py`.

---

## 2. Protokol *Three-Way-Scan* (`WHY / HOW / WHAT`)

Setiap artikel ilmiah yang dibedah wajib diekstrak ke dalam struktur 3 dimensi berikut agar siap menjadi bahan kajian literatur dan komparasi *State of the Art*:

| Dimensi | Pertanyaan Kunci yang Harus Dijawab | Yang Harus Dicatat Secara Spesifik |
| :--- | :--- | :--- |
| **WHY** *(Mengapa diteliti?)* | Masalah spesifik apa yang ingin diselesaikan, dan apa kelemahan pendekatan sebelumnya? | Konteks domain, *bottleneck* utama, dan rumusan celah riset (*research gap*) yang diklaim penulis. |
| **HOW** *(Bagaimana caranya?)* | Arsitektur, algoritma, metode pengembangan, instrumen, atau konfigurasi pengujian apa yang digunakan? | Tech stack/algoritma, skema data, jumlah sampel/skenario uji, variabel kontrol, dan metrik evaluasi. |
| **WHAT** *(Apa temuannya & batasannya?)* | Apa hasil kuantitatif/kualitatif utamanya, dan apa keterbatasan yang belum diselesaikan oleh studi tersebut? | Angka hasil eksperimen (waktu respons, akurasi, throughput, nilai *p*), kesimpulan utama, dan **celah yang ditinggalkan untuk penelitian Anda**. |

### Format Tabel Matriks Sintesis Literatur

Sajikan hasil bedah beberapa paper ke dalam tabel perbandingan:

| No | Peneliti & Tahun | Judul & Publikasi | WHY (Masalah & Konteks) | HOW (Metode / Arsitektur / Pengujian) | WHAT (Temuan Kuantitatif) | Keterbatasan / Research Gap terhadap Riset Kita |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- |

---

## 3. Mode *Socratic Mentor* & Deteksi Niat (*Intent Detection*)

Saat mendampingi peneliti merumuskan masalah (RQ) atau merancang metodologi:

1. **Deteksi Niat (*Exploratory* vs *Goal-Oriented*)**:
   - **Eksploratif**: Jika peneliti masih menggali ide atau membandingkan opsi desain, **jangan terburu-buru menutup diskusi** atau langsung mencetak draf panjang. Ajukan 1–2 pertanyaan tajam yang menguji asumsi dasar (*trade-off* arsitektur, ancaman validitas, atau kelayakan pengujian).
   - **Berorientasi Target (*Goal-Oriented*)**: Jika peneliti sudah memiliki keputusan desain dan meminta kerangka/blueprint, susun *RQ Brief* dan *Methodology Blueprint* secara langsung.
2. **Indikator Kesehatan Dialog (*Dialogue Health Check*)**:
   - Setiap beberapa putaran diskusi, periksa apakah agen terlalu sering langsung setuju (*persistent agreement*) atau menghindari konflik logika. Jika ada asumsi metodologi peneliti yang berisiko ditolak penguji/reviewer, angkat keberatan tersebut secara konstruktif.
