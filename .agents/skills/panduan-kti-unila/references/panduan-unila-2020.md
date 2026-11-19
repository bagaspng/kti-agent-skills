# Panduan Penulisan Karya Ilmiah Universitas Lampung (Edisi Revisi ke-5, 2020)

Berkas rujukan ini merangkum ketentuan tata letak fisik, tipografi, penomoran halaman, penyajian tabel/gambar, dan kaidah penulisan berdasarkan **Buku Panduan Penulisan Karya Ilmiah Universitas Lampung (Tahun 2020)**.

---

## 1. Spesifikasi Kertas, Sampul, dan Sembir (Margin)

1. **Ukuran & Jenis Kertas**:
   - Kertas HVS putih ukuran **A4 (21,0 cm × 29,7 cm)**, bobot **80 gram** (untuk Skripsi, Tesis, Disertasi) atau 70 gram (Laporan KP/PKL).
2. **Sampul Luar (*Hard Cover*)**:
   - Kertas *buffalo* dijilid tebal (*hard cover*), tulisan dicetak dengan tinta emas.
   - **Warna Sampul Fakultas Teknik (FT Unila)**: **Biru Tua** (*Navy/Dark Blue*, kode RGB `00 00 8B`).
3. **Batas Sembir (Margin Halaman)**:
   - **Sembir Kiri**: **4,0 cm** (area penjilidan)
   - **Sembir Atas**: **3,0 cm**
   - **Sembir Kanan**: **3,0 cm**
   - **Sembir Bawah**: **3,0 cm**
   - Jarak *header* dan *footer* dari tepi kertas: **1,5 cm**.
   - Seluruh isi naskah (termasuk tabel, gambar, diagram, dan persamaan) tidak boleh melewati batas sembir.

---

## 2. Tipografi dan Spasi Baris

1. **Jenis dan Ukuran Huruf**:
   - Seluruh naskah wajib menggunakan huruf **Times New Roman ukuran 12 pt** berwarna hitam pekat (`RGB 0, 0, 0`).
   - Termasuk judul bab (`BAB I PENDAHULUAN`), judul subbab (`1.1 Latar Belakang`), isi paragraf, judul tabel, judul gambar, dan daftar pustaka semuanya berukuran **12 pt** (tidak boleh memperbesar judul bab menjadi 14 pt).
   - Pengecualian ukuran huruf: isi di dalam sel tabel yang padat boleh menggunakan ukuran **10–11 pt** agar muat dalam margin.
2. **Cetak Miring (*Italic*)**:
   - Wajib digunakan untuk istilah asing/bahasa daerah yang belum diserap ke dalam KBBI (contoh: *backend*, *frontend*, *endpoint*, *framework*, *load testing*, *black box testing*, *role-based access control*, *modular monolith*, *signature pad*) serta nama ilmiah spesies.
3. **Jarak Antarbaris (Spasi Vertikal)**:
   - **Spasi 1,5**: Digunakan untuk seluruh paragraf narasi batang tubuh tulisan.
   - **Spasi 1,0 (Spasi Tunggal)**:
     - Isi Abstrak dan *Abstract*;
     - Judul bab dan judul subbab yang lebih dari satu baris;
     - Judul tabel dan judul gambar yang lebih dari satu baris;
     - Teks di dalam sel tabel;
     - Kutipan langsung yang panjangnya lebih dari 3 baris;
     - Tiap entri di dalam Daftar Pustaka (dengan jarak antar-entri pustaka sebesar 1 baris kosong / `12 pt`).
4. **Jarak Khusus Antar-Elemen**:
   - **Judul BAB**: Diketik dengan huruf kapital semua, tebal (**Bold**), rata tengah (*Center*), dimulai **6 cm dari tepi atas kertas** (sembir atas 3 cm + jarak spasi sebelum judul 3 cm atau `~85 pt`).
   - **Judul BAB ke baris pertama teks atau subbab**: Berjarak **4 spasi** (`24 pt` setelah judul bab).
   - **Antara teks dan tabel/gambar**: Berjarak **3 spasi** (`18 pt`).
5. **Paragraf & Indentasi**:
   - Perataan paragraf batang tubuh: **Rata Kiri-Kanan (*Justify*)**.
   - Baris pertama setiap paragraf baru menjorok ke dalam sebesar **1,0 cm** (`first_line_indent = 1.0 cm`). Paragraf butir bernomor/berhuruf tidak diberi `first_line_indent` tambahan di luar indentasi butirnya.
   - Hindari *orphan/widow*: judul subbab di bagian bawah halaman harus diikuti minimal **2 baris teks** sebelum berganti halaman (`keep_with_next = True`).

---

## 3. Sistem Penomoran Halaman Ganda (Khas Unila)

Penomoran halaman menggunakan huruf **Times New Roman 12 pt** dengan aturan tiga zona:

| Zona Dokumen | Cakupan Bagian | Format Nomor | Posisi Cetak Nomor Halaman |
| :--- | :--- | :--- | :--- |
| **Zona 0: Sampul & Halaman Judul** | Halaman Sampul Luar, Halaman Judul Dalam, Lembar Pengesahan | Dihitung namun tidak dicetak | **Tidak ditampilkan** (*header* & *footer* kosong) |
| **Zona 1: Bagian Awal (Halaman Pemula)** | Abstrak, *Abstract*, Prakata/Kata Pengantar, Daftar Isi, Daftar Tabel, Daftar Gambar, Daftar Lampiran | **Angka Romawi kecil** (`i, ii, iii, iv, ...`) | **Kanan Bawah** (*Footer* rata kanan, 1,5 cm dari tepi bawah, 3 cm dari tepi kanan) |
| **Zona 2: Bagian Utama & Akhir** | Bab I s.d. Bab V, Daftar Pustaka, Lampiran | **Angka Arab** (`1, 2, 3, ...`) | **Kanan Atas** (*Header* rata kanan, 1,5 cm dari tepi atas, 3 cm dari tepi kanan), **KECUALI** halaman pertama tiap BAB dan Daftar Pustaka yang nomornya dihitung tetapi **tidak dicetak** (`different_first_page_header_footer = True`) |

---

## 4. Penomoran Bab, Subbab, Tabel, Gambar, dan Persamaan

1. **Hierarki Bab dan Subbab**:
   - **Level 1 (Bab)**: `BAB I PENDAHULUAN`, `BAB II TINJAUAN PUSTAKA`, `BAB III METODOLOGI PENELITIAN`, `BAB IV HASIL DAN PEMBAHASAN`, `BAB V SIMPULAN DAN SARAN` (Angka Romawi kapital, huruf kapital seluruhnya, tebal, rata tengah, tanpa tanda titik di akhir).
   - **Level 2 (Subbab)**: `1.1 Latar Belakang`, `2.1 Regulasi Sertifikasi` (Angka Arab `bab.urut` **tanpa titik di belakang angka terakhir**, *Title Case*, tebal, rata kiri, tanpa titik di akhir judul).
   - **Level 3 (Anak Subbab)**: `3.4.1 Analisis Kebutuhan` (Angka Arab `bab.sub.urut` **tanpa titik di belakang angka terakhir**, *Title Case*, tebal, rata kiri, tanpa titik di akhir judul).
2. **Penyajian dan Judul Tabel**:
   - Nomor tabel mengikat pada bab: `Tabel 2.1`, `Tabel 3.1` (bukan nomor urut tunggal `Tabel 1`, `Tabel 2`).
   - **Posisi Judul Tabel**: Di **atas** tabel, rata kiri (*Left*), spasi 1,0, `keep_with_next = True`.
   - **Aturan Titik Judul Tabel**: Judul tabel **TIDAK BOLEH diakhiri tanda titik** (contoh benar: `Tabel 3.1 Jadwal Pelaksanaan Penelitian`).
   - Jika tabel terpotong lintas halaman, halaman lanjutan diberi judul `Tabel 3.1 (lanjutan)` dan baris *header* tabel diulang (`tblHeader`).
   - Garis tabel mengutamakan garis horizontal atas, garis pemisah kepala tabel, dan garis penutup bawah.
3. **Penyajian dan Judul Gambar**:
   - Nomor gambar mengikat pada bab: `Gambar 2.1.`, `Gambar 3.1.`
   - **Posisi Gambar & Judul Gambar**: Gambar diletakkan rata tengah (*Center*). Judul gambar diletakkan di **bawah** gambar, rata tengah (*Center*), spasi 1,0.
   - **Aturan Titik Judul Gambar**: Judul gambar **WAJIB diakhiri tanda titik (`.`)** (contoh benar: `Gambar 3.1. Alur penelitian.`).
   - Sumber gambar (jika dikutip dari pustaka lain) dicantumkan pada akhir judul gambar sebelum titik akhir.
4. **Persamaan Matematika**:
   - Diketik rata tengah atau menjorok, dengan nomor persamaan di tepi kanan dalam tanda kurung mengikat pada bab: `(2.1)`, `(3.1)`.

---

## 5. Daftar Isi, Daftar Tabel, Daftar Gambar, dan Daftar Pustaka

1. **Daftar Isi, Daftar Tabel, Daftar Gambar**:
   - Judul `DAFTAR ISI`, `DAFTAR TABEL`, dan `DAFTAR GAMBAR` diketik kapital, tebal, rata tengah.
   - Di bawah judul, terdapat baris label kolom `Halaman` di tepi kanan (dan label `Tabel` / `Gambar` di tepi kiri untuk Daftar Tabel/Gambar).
   - Setiap entri dihubungkan dengan titik-titik penuntun (*dot leader tab stop* pada posisi `14,0 cm` untuk lebar area teks A4 dengan margin kiri 4 cm dan kanan 3 cm) menuju nomor halaman asli.
2. **Daftar Pustaka**:
   - Menggunakan minimal **80% pustaka primer** (artikel jurnal ilmiah nasional terakreditasi/internasional bereputasi, prosiding, paten, standar teknis resmi) dari 5–10 tahun terakhir.
   - Setiap pustaka yang tertulis di Daftar Pustaka **wajib** disitir di dalam batang tubuh tulisan, dan setiap sitasi di batang tubuh **wajib** ada di Daftar Pustaka.
   - Diketik dengan spasi 1,0 di dalam satu pustaka dan jarak `12 pt` (spasi ganda) antar-pustaka, menggunakan *hanging indent* `1,0 cm` (atau tab stop rata kiri `1,0 cm` untuk penomoran IEEE `[1]`).
