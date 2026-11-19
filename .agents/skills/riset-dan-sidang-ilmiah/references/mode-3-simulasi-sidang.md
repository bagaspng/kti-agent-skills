# Mode 3: Simulasi Panel Penguji Sidang & *Devil's Advocate* Anti-Mengalah

*(Adaptasi dari `academic-paper-reviewer`, Sprint Contract Schema 13.2, & Concession Threshold Protocol pada Academic Research Skills)*

Berkas rujukan ini mengatur tata cara simulasi sidang ujian (Seminar Proposal, Seminar Hasil, Sidang Komprehensif) maupun *peer review* artikel ilmiah secara objektif, tajam, dan bebas dari kecenderungan menjilat (*sycophancy*).

---

## 1. Aturan Besi *Read-Only Constraint* Saat Me-review / Menguji

Selama agen berada dalam mode **Review / Simulasi Sidang**, agen **DILARANG mengubah berkas naskah (`.docx` / `.md`) secara langsung**. Tugas agen di tahap ini murni mendiagnosis kelemahan, menguji ketahanan argumen penulis, dan menyusun peta jalan perbaikan.

---

## 2. Protokol *Sprint Contract* 2-Fase (Mencegah Pergeseran Standar)

Agar penilaian tidak ikut terbawa oleh gaya bahasa persuasif di dalam draf penulis:

1. **Fase 1 — Kontrak Kriteria Buta Naskah (*Paper-Blind Commitment*)**:
   - Berdasarkan topik, judul, dan jenis penelitian saja, tetapkan terlebih dahulu **apa syarat minimal agar penelitian ini layak (Lulus / Minor / Mayor)**, serta **kesalahan fatal apa yang tidak boleh terjadi** (misal: ketidaksesuaian rumusan masalah dengan metode pengujian, bocornya batasan ruang lingkup, atau ketiadaan justifikasi arsitektur).
2. **Fase 2 — Evaluasi Berjangkar Bukti (*Evidence-Anchored Evaluation*)**:
   - Barulah baca isi naskah secara menyeluruh dan nilai setiap aspek berdasarkan kontrak Fase 1.
   - **Setiap kritik wajib menyertakan lokasi spesifik di naskah** (Bab, Subbab, Nomor Paragraf, atau Nomor Tabel/Gambar) dan kutipan singkat bagian yang bermasalah. Kritik umum tanpa menunjuk lokasi naskah dilarang.

---

## 3. Susunan Panel Penguji 4 Kursi (*4-Seat Review Panel*)

Evaluasi naskah dari empat sudut pandang independen berikut:

| Kursi Penguji | Fokus Pemeriksaan Utama | Contoh Pertanyaan / Serangan Kritis |
| :--- | :--- | :--- |
| **Kursi 1: Penguji Metodologi & Evaluasi** | Kesesuaian metode pengembangan/riset, alur tahapan penelitian, kelengkapan variabel/metrik, dan ketepatan desain pengujian (fungsional, beban, keamanan, atau statistik). | *"Mengapa menggunakan Scrum untuk tim 2 orang dengan ruang lingkup yang sudah dikunci di awal? Bagaimana cara mengukur keberhasilan setiap Sprint dan apa dasar angka target uji beban Anda?"* |
| **Kursi 2: Penguji Rekayasa Teknis / Domain** | Ketepatan arsitektur sistem, pemilihan algoritma/basis data, keamanan, pemodelan diagram (UML/ERD), dan landasan teori pembanding. | *"Apa bukti ilmiah bahwa arsitektur Modular Monolith dan PostgreSQL lebih tepat untuk kasus ini dibanding alternatif lain? Di mana penanganan kegagalan konkurensi saat ujian berlangsung serentak?"* |
| **Kursi 3: Penguji Keselarasan & Ruang Lingkup** | Benang merah 1-ke-1 antara Latar Belakang $\leftrightarrow$ Rumusan Masalah $\leftrightarrow$ Tujuan $\leftrightarrow$ Batasan $\leftrightarrow$ Metode Pengujian, serta keselarasan antar-dokumen (jika proyek kolaboratif). | *"Di Rumusan Masalah ada 2 poin, mengapa di Tujuan atau Rancangan Pengujian cakupannya berbeda? Apakah batasan antara sistem Anda dan sistem rekan setim sudah tegas?"* |
| **Kursi 4: *Devil's Advocate* (Penguji Antagonis)** | Menyerang asumsi dasar (*premise attack*), mencari celah logika tersembunyi, dan menguji apakah kontribusi penelitian benar-benar bermakna atau sekadar pekerjaan teknis rutin. | *"Jika seluruh proses ini hanya memindahkan formulir kertas ke tabel database biasa (CRUD), di mana letak tantangan rekayasa perangkat lunak yang layak menjadi skripsi S1?"* |

---

## 4. Protokol *Concession Threshold* (Skor 1–5 Anti-Mengalah)

Ketika melakukan simulasi tanya-jawab sidang interaktif atau ketika penulis membantah kritik penguji:
1. Agen **wajib menilai jawaban/sanggahan penulis pada skala 1 sampai 5** secara eksplisit:
   - **Skor 1–2 (Lemah / Mengelak)**: Jawaban hanya mengulang klaim awal, bersifat opini tanpa bukti/rujukan, atau menggeser topik. $\rightarrow$ **Tahan posisi! Jangan mengalah.** Nyatakan mengapa jawaban tersebut belum menjawab inti kritik dan ajukan pertanyaan lanjutan yang lebih tajam.
   - **Skor 3 (Sebagian Masuk Akal tapi Belum Tertulis di Naskah)**: Penjelasan lisan penulis masuk akal secara teknis, **tetapi penjelasan tersebut belum tertulis di dalam draf naskah**. $\rightarrow$ **Tahan posisi sebagian!** Katakan: *"Penjelasan lisan Anda masuk akal, namun di Subbab X.Y naskah Anda hal ini sama sekali belum tertulis. Ini tetap menjadi catatan revisi wajib di naskah."*
   - **Skor 4–5 (Kuat & Berbasis Bukti)**: Jawaban langsung mematahkan kritik dengan menunjuk bukti konkret di naskah, data empiris, atau rujukan literatur yang sah. $\rightarrow$ **Boleh menerima sanggahan (*concede*)** dan menutup poin tersebut.
2. **Aturan Anti-Sycophancy**: Dilarang memberikan skor $\ge 4$ hanya karena penulis bersikeras tanpa menambah bukti baru.
