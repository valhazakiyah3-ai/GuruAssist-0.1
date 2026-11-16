# GuruAssist

**Asisten AI untuk administrasi guru dan perencanaan pembelajaran.** GuruAssist adalah proyek open-source berbasis format Agent Skills yang membantu guru mengumpulkan konteks pembelajaran sekali, lalu menggunakannya kembali untuk menyusun dokumen yang diminta.

**Status:** rilis awal `v0.1.0` · **Lisensi:** MIT · **Bahasa utama:** Indonesia

## Fitur saat ini

- Menyusun draf rencana pembelajaran/modul ajar untuk berbagai mata pelajaran.
- Membantu membuat LKPD, bahan ajar, instrumen asesmen, rubrik, dan metadata platform sesuai permintaan.
- Memeriksa keselarasan tujuan, aktivitas, bukti belajar, dan asesmen.
- Memakai panduan PAI khusus untuk Pendidikan Agama Islam dan Budi Pekerti.
- Memvalidasi data pembelajaran berbentuk JSON dan mengekspor draf rancangan pembelajaran ke DOCX.
- Menandai informasi yang belum tersedia atau perlu diperiksa guru.

## Batas kemampuan

- GuruAssist adalah skill/panduan kerja untuk AI agent yang kompatibel dengan Agent Skills; GitHub hanya menyimpan dan mendistribusikan berkasnya, bukan menjalankan skill secara otomatis.
- Skrip DOCX hanya memformat data yang sudah disediakan. Skrip tidak memanggil model AI, menyusun isi pedagogis secara mandiri, atau memverifikasi kebenaran kurikulum.
- GuruAssist tidak mengklaim memiliki koneksi atau akses langsung ke Ruang GTK, PMM, atau platform pemerintah lain. Metadata disiapkan agar dapat ditinjau dan disalin oleh guru.
- Hasil adalah draf. Guru tetap bertanggung jawab memeriksa sumber, kebijakan sekolah, kebutuhan peserta didik, dan kesesuaian kurikulum.
- Tidak semua dokumen atau fitur pada platform pendidikan otomatis wajib diisi oleh setiap guru.

## Struktur repository

```text
guruassist/
├── .github/workflows/tests.yml
├── tests/test_scripts.py
├── skills/teacher-administration/
│   ├── SKILL.md
│   ├── references/       # Panduan umum, asesmen, PAI, allowlist kitab, dan batas platform
│   ├── templates/        # Modul ajar, LKPD, rubrik, metadata generik
│   ├── scripts/          # Validator JSON dan generator DOCX
│   ├── examples/         # Template input dan contoh sintetis PAI
│   └── evals/            # Kasus evaluasi perilaku skill
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── requirements.txt
```

## Persyaratan

- Agent yang digunakan harus mendukung Agent Skills atau mekanisme pemuatan skill yang kompatibel.
- Python 3.9 atau lebih baru untuk skrip.
- `python-docx` untuk ekspor DOCX.

## Memasang skill

1. Unduh repository sebagai ZIP atau clone repository.
2. Salin folder `skills/teacher-administration/` ke direktori skill milik agent yang digunakan.
3. Muat ulang/restart agent bila diperlukan.
4. Minta agent membantu menyusun rencana pembelajaran, misalnya: `Bantu susun modul ajar IPA kelas VIII tentang tekanan zat. Saya akan mengunggah CP dan format sekolah.`

Lokasi direktori skill berbeda pada setiap aplikasi agent. Ikuti dokumentasi aplikasi yang digunakan.

## Mencoba contoh

Pasang dependensi:

```bash
python -m pip install -r requirements.txt
```

Validasi contoh PAI:

```bash
python skills/teacher-administration/scripts/validate_lesson_data.py \
  skills/teacher-administration/examples/pai-salat-berjamaah.json
```

Buat dokumen DOCX:

```bash
python skills/teacher-administration/scripts/generate_docx.py \
  skills/teacher-administration/examples/pai-salat-berjamaah.json \
  --output output/modul-ajar-draft.docx
```

Mulai dari template JSON umum:

`skills/teacher-administration/examples/lesson-input-template.json`

Ganti teks contoh dengan data yang benar. Isi capaian/standar hanya dari dokumen resmi atau sumber yang benar-benar tersedia. Simpan file JSON, lalu jalankan validator dan generator seperti contoh di atas.

## Menjalankan tes

Pasang dependensi pengembangan lalu jalankan tes:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

GitHub Actions menjalankan tes pada Python 3.9, 3.11, dan 3.13 setiap ada push atau pull request.

## Prinsip desain

1. **Satu sumber data:** informasi inti pembelajaran dikumpulkan sekali dan dipakai ulang.
2. **Guru tetap memegang kendali:** semua keluaran substantif adalah draf untuk ditinjau.
3. **Tidak mengarang aturan:** jangan menyatakan sesuatu wajib tanpa sumber kurikulum/kebijakan yang berlaku.
4. **Adaptif lintas mata pelajaran:** gunakan panduan PAI hanya untuk tugas PAI; mata pelajaran lain mengikuti sumber dan standar yang disediakan.
5. **Privasi sejak awal:** gunakan data agregat dan hindari identitas pribadi peserta didik.
6. **Integrasi secara jujur:** siapkan metadata salin-tempel kecuali tersedia integrasi resmi, diizinkan, dan teruji.

## Kontribusi

Baca [CONTRIBUTING.md](CONTRIBUTING.md). Kontribusi template anonim, referensi mata pelajaran yang dapat ditelusuri, kasus evaluasi, dan perbaikan aksesibilitas sangat terbuka.

## Lisensi

MIT. Lihat [LICENSE](LICENSE).
