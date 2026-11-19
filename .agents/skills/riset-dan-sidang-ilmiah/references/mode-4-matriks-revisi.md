# Mode 4: *Revision Coach*, Audit Sanggahan, & Matriks Ketertelusuran Revisi (*R&R Traceability Matrix*)

*(Adaptasi dari `revision_coach_agent`, `rebuttal-audit`, & Schema 11 R&R Matrix pada Academic Research Skills)*

Berkas rujukan ini digunakan ketika penulis menerima daftar catatan revisi dari dosen pembimbing, dosen penguji seminar/sidang, atau *reviewer* jurnal, maupun setelah selesai menjalankan Mode 3 (Simulasi Sidang).

---

## 1. Alur Kerja *Revision Coach* (Dari Catatan Mentah ke Peta Jalan)

Jangan langsung mengubah naskah secara membabi buta ketika menerima daftar revisi. Jalankan 4 langkah terstruktur berikut:

1. **Dekomposisi & Klasifikasi Catatan Revisi**:
   - Pecah setiap kalimat/butir catatan dosen menjadi item atomik bernomor (`REV-01`, `REV-02`, dst.).
   - Klasifikasikan tingkat dampaknya:
     - **`STRUKTURAL / MAYOR`**: Memerlukan perubahan urutan subbab, penambahan/penggantian gambar diagram, penyelarasan tabel jadwal/tim, atau penambahan landasan literatur baru.
     - **`SUBSTANSI LOKAL`**: Memerlukan penambahan 1–2 paragraf penjelasan atau penajaman kalimat pada subbab tertentu.
     - **`MINOR / EDITORIAL`**: Perbaikan istilah, salah ketik, penomoran tabel/gambar, atau kerapian daftar pustaka.
2. **Identifikasi Efek Domino Antarbab (*Cross-Chapter ImpactCheck*)**:
   - Setiap kali satu poin diubah, periksa dampaknya ke seluruh bab lain!
   - *Contoh*: Jika rentang bulan penelitian di `Tabel 3.1` diubah dari 6 bulan menjadi 5 bulan, maka narasi di `Bab II` (alasan pemilihan metode Scrum) dan `Bab III Subbab 3.2` juga **wajib** ikut diperbarui agar tidak timbul kontradiksi internal.
   - *Contoh*: Jika jumlah aktor pada *Use Case Diagram* diubah, maka `Bab I Batasan Masalah`, `Bab II`, dan `Bab III` wajib diperiksa seluruhnya.
3. **Konsultasi Keputusan (*Decision Tree*)**:
   - Jika ada poin revisi yang memiliki lebih dari satu cara penyelesaian (misal: memilih rujukan pembanding arsitektur atau menyepakati pembagian tugas dengan rekan satu proyek), tanyakan opsi keputusannya kepada penulis sebelum mengeksekusi.

---

## 2. Standar Tabel Matriks Ketertelusuran Revisi (*R&R Traceability Matrix* — Schema 11)

Setiap sesi revisi wajib menghasilkan atau memperbarui tabel matriks berikut agar penulis dan dosen pembimbing dapat memverifikasi setiap perubahan dengan mudah:

| ID | Poin Revisi Dosen / Penguji | Kategori | Rencana / Klaim Perbaikan | Lokasi Spesifik di Naskah (Bab / Subbab / Tabel / Gambar) | Efek Domino yang Ikut Diperiksa | Status Verifikasi |
| :-: | :--- | :-: | :--- | :--- | :--- | :-: |
| `REV-01` | *[Kutipan catatan revisi]* | Mayor / Lokal / Minor | *[Penjelasan konkret apa yang ditambahkan/diubah]* | `Bab III, Subbab 3.1 & Gambar 3.1` | `Daftar Gambar, Bab I Sistematika` | `TERVERIFIKASI` / `BELUM` |

---

## 3. Protokol *Rebuttal & Re-Review Audit* (Verifikasi Pasca-Revisi)

Setelah draf selesai direvisi, jalankan pemeriksaan verifikasi ulang (*Stage 3' Re-Review*):
1. **Cek Kebenaran Klaim Revisi**: Apakah perubahan yang diklaim pada kolom *Rencana/Klaim Perbaikan* di Matriks R&R benar-benar sudah tertulis di dalam berkas naskah terbaru? (Jangan pernah menandai `TERVERIFIKASI` jika teksnya belum ada di berkas).
2. **Cek Regresi Baru**: Apakah penambahan paragraf/gambar baru menyebabkan penomoran tabel/gambar bergeser, sitasi baru belum masuk ke Daftar Pustaka, atau menimbulkan kontradiksi dengan paragraf di atas/bawahnya?
