# Profil Gaya Selingkung S1 Teknik Informatika FT Unila & Konvensi Skripsi Kolaboratif

Berkas ini memuat aturan khusus Program Studi S1 Teknik Informatika, Jurusan Teknik Elektro, Fakultas Teknik Universitas Lampung, termasuk konvensi untuk penelitian rekayasa perangkat lunak (RPL) kolaboratif (*Backend* dan *Frontend*).

---

## 1. Gaya Sitasi dan Daftar Pustaka (IEEE Numbered Style)

1. **Format Sitasi dalam Teks (Batang Tubuh)**:
   - Menggunakan sistem penomoran berurut **IEEE** di dalam kurung siku: `[1]`, `[2]`, `[3]–[5]`, `[12], [15]`.
   - Nomor sitasi diurutkan berdasarkan kemunculan pertama di dalam naskah mulai dari Bab I.
   - Contoh penulisan:
     - Di akhir klaim: `... menggunakan arsitektur client–server berbasis RESTful API [17], [26].`
     - Menyebut nama penulis: `Blinowski dkk. [65] membandingkan performa arsitektur monolitik dan microservices...` (untuk 3 penulis atau lebih dalam teks bahasa Indonesia, gunakan `dkk.`, bukan `et al.`).
2. **Format Entri Daftar Pustaka (IEEE)**:
   - Setiap item diawali nomor `[n]` diikuti tab (`1,0 cm` *hanging indent*), inisial nama depan lalu nama belakang penulis, judul karya dalam tanda kutip `"..."`, nama jurnal/konferensi dicetak miring (*italic*), volume, nomor, halaman, dan tahun.
   - Di dalam `DAFTAR PUSTAKA` berbahasa Inggris/internasional, kata hubung antar-penulis tetap menggunakan `and` / `et al.` sesuai standar IEEE.

---

## 2. Struktur Bab & Subbab Standar Skripsi RPL Teknik Informatika Unila

### Bab I: Pendahuluan
- `1.1 Latar Belakang`: Disusun dengan pola piramida terbalik (Konteks makro & regulasi $\rightarrow$ Kondisi lapangan/*As-Is* di mitra $\rightarrow$ Masalah teknis/operasional $\rightarrow$ *Research gap* penelitian terdahulu $\rightarrow$ Solusi yang diusulkan).
- `1.2 Rumusan Masalah`: Kalimat tanya terukur yang memetakan perancangan/implementasi dan evaluasi/pengujian.
- `1.3 Tujuan`: Kalimat pernyataan yang berkorespondensi 1-ke-1 dengan rumusan masalah.
- `1.4 Batasan Masalah`: Mempertegas lingkup sistem (misal: fokus *backend* vs *frontend*, jumlah aktor, jenis pengujian, mekanisme tanda tangan, batas lingkungan deployment).
- `1.5 Manfaat`: Manfaat praktis bagi mitra/aktor dan manfaat akademis.
- `1.6 Sistematika Penulisan`: Ringkasan isi Bab I s.d. Bab V.

### Bab II: Tinjauan Pustaka
- Subbab landasan teori disusun mengalir dari domain masalah menuju arsitektur, teknologi inti, metode pengembangan, pemodelan UML, dan metode pengujian.
- **Justifikasi Pemilihan Arsitektur & Teknologi**: Setiap pilihan arsitektur utama (misal: *Client–Server* vs Monolitik Terpadu, *Modular Monolith* vs *Microservices*, *RESTful API* vs *GraphQL*, *Laravel* vs *Express.js*, *PostgreSQL* vs *MySQL*) harus disertai landasan literatur pembanding yang menjawab pertanyaan penguji.
- **Subbab Penelitian Terdahulu**:
  - Wajib memisahkan tabel ringkasan menjadi dua tabel terpisah apabila mencakup literatur dalam dan luar negeri:
    1. **Tabel Penelitian Terdahulu (Literatur Nasional)** (minimal 5–6 jurnal nasional terakreditasi SINTA);
    2. **Tabel Penelitian Terdahulu (Literatur Internasional)** (minimal 5–6 jurnal/prosiding internasional bereputasi IEEE/Scopus).
  - Narasi pembahasan penelitian terdahulu merangkum persamaan, keterbatasan (*research gap*), dan posisi kebaruan penelitian yang diusulkan.

### Bab III: Metodologi Penelitian
Urutan subbab standar yang disepakati pada Prodi Teknik Informatika FT Unila:
1. `3.1 Alur Penelitian`:
   - Diletakkan di **bagian paling awal Bab III** (sebelum Waktu dan Tempat Penelitian), dilengkapi **Gambar 3.1. Alur penelitian.** (7 tahapan mulai dari identifikasi masalah/kebutuhan, perancangan, pelaksanaan sprint, integrasi sistem, pengujian akhir, hingga penyusunan laporan).
2. `3.2 Waktu dan Tempat Penelitian`:
   - Menyebutkan rentang bulan pelaksanaan secara konsisten (sama persis dengan Bab II alasan pemilihan metode dan **Tabel 3.1 Jadwal Pelaksanaan Penelitian**) serta lokasi penelitian.
3. `3.3 Bahan dan Alat`:
   - Terbagi menjadi `3.3.1 Bahan Penelitian` (data primer/sekunder mitra) dan `3.3.2 Alat Penelitian` (**Tabel 3.2 Perangkat Keras dan Perangkat Lunak Penelitian**, termasuk spesifikasi server *deployment*/VPS jika di-hosting).
4. `3.4 Metode Penelitian` (Kerangka Kerja *Scrum*):
   - Menampilkan struktur tim (**Gambar 3.2. Struktur Tim Scrum.** dan **Tabel 3.3 Susunan Tim Scrum**: *Product Owner*, *Scrum Master*, *Developer*).
   - Menguraikan tahapan `3.4.1 Analisis Kebutuhan` (Tabel Kebutuhan Fungsional/*Product Backlog* & Tabel Kebutuhan Nonfungsional), `3.4.2 Perancangan Sistem` (Diagram Use Case berbahasa Indonesia & Diagram Arsitektur Sistem), serta `3.4.3 Pelaksanaan Sprint` (*Sprint Planning*, *Sprint Execution*, *Sprint Review*, *Sprint Retrospective* beserta Tabel Rencana Sprint & Tabel Pembagian Kerja Tim per Sprint).
5. `3.5 Metode Pengujian`:
   - Menguraikan pengujian fungsional (*Black Box Testing* dengan *Equivalence Partitioning* & *Boundary Value Analysis*), pengujian keamanan (*Security Testing* berdasarkan OWASP API Security Top 10), dan pengujian kinerja (*Load Testing* dengan Grafana k6).

---

## 3. Aturan Khusus Proyek Kolaboratif (Backend vs Frontend) & Diagram UML

1. **Pemisahan Batas Cakupan (*Scope Boundary*) Backend vs Frontend**:
   - Pada **Diagram Arsitektur Sistem Backend**, sisi *frontend* cukup digambarkan sebagai satu kotak batas eksternal (misal: *"Klien Web (dikembangkan pada skripsi terpisah)"*) tanpa merinci komponen internal UI (*State Management*, komponen React/Vue, dll.). Sebaliknya, skripsi *frontend* tidak merinci internal *layer* *backend*.
2. **Keselarasan Antar-Dokumen Satu Tim Proyek**:
   - Antara skripsi *Backend* dan *Frontend* yang berada dalam satu proyek kolaboratif, elemen berikut **wajib identik dan sinkron**:
     - Rentang bulan dan baris tahapan pada **Tabel 3.1 Jadwal Pelaksanaan Penelitian**;
     - Bentuk visual **Gambar Alur Penelitian**, **Gambar Siklus Scrum**, **Gambar Hierarki Skema**, dan **Gambar Gaya Arsitektur Client–Server**;
     - Jumlah dan nama peran aktor utama pada **Use Case Diagram**;
     - Pembagian peran pada **Tabel Susunan Tim Scrum** (*Product Owner*, *Scrum Master*, *Developer*) dan bentuk *deployment* (Server Hosting VPS).
3. **Pembagian Diagram UML (Structure vs Behavioral) & Bahasa**:
   - *Use Case Diagram* dan *Diagram Arsitektur* disajikan pada **Bab III** untuk mendefinisikan batas fungsional awal, sedangkan *Entity Relationship Diagram (ERD)* (*Structure Diagram*) serta *Activity Diagram* dan *Sequence Diagram* (*Behavioral Diagrams*) disajikan secara rinci pada **Bab IV (Hasil dan Pembahasan)**.
   - **Seluruh label dan notasi di dalam gambar diagram wajib menggunakan Bahasa Indonesia** (istilah asing di dalam penjelasan teks dicetak miring).

---

## 4. Konvensi Penamaan Versi Berkas & Arsip (`backup/`)

1. Di dalam *root folder* ruang kerja skripsi, **hanya boleh ada satu berkas draf aktif terbaru** dengan penomoran inkremental:
   - `draft_skripsi_p1.docx` $\rightarrow$ `draft_skripsi_p2.docx` $\rightarrow$ `draft_skripsi_p3.docx`, dst.
2. Sebelum menulis versi baru `p(N+1)`, berkas versi sebelumnya `pN` **wajib disalin/dipindahkan terlebih dahulu ke folder `backup/`** agar *root folder* selalu bersih dan riwayat revisi aman.
