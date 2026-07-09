# Missing Plant Data Experiments

## Tujuan Eksperimen Data Top-View

Eksperimen data bertujuan menentukan format input, altitude, speed, pola terbang, dan kondisi pencahayaan yang paling memungkinkan plot bolong / missing plant terlihat jelas pada kebun nanas. Hasil eksperimen dipakai untuk memperbaiki strategi pengambilan data, bukan untuk mengklaim akurasi model final.

Case ini berbasis pola tanaman dari atas, sehingga dataset awal paling relevan berupa top-view/nadir video frame, foto drone, atau orthomosaic `.tif`. Tahap saat ini belum memakai dataset publik. Dataset asli akan diminta dari pembimbing atau tim GGP/GGF terlebih dahulu agar data lebih sesuai dengan kondisi lapangan, komoditas nanas, sudut kamera, dan target operasional.

## Status Dataset

- Belum ada dataset asli lapangan yang masuk ke repository.
- Tidak ada rencana menambahkan dataset publik pada tahap ini.
- Tidak ada auto-download dataset, Roboflow, Kaggle, Mendeley, API key, token, cloud, atau S3.
- Pipeline tetap offline dan lokal sampai pembimbing/tim memberikan contoh data.
- Dukungan image folder, `.tif`/GeoTIFF tiling, preprocessing, anotasi, dan model asli baru diputuskan setelah contoh data diterima.

## Checklist Request Data Ke Pembimbing/Tim

- Jenis data yang tersedia: video, foto/frame, `.tif`, orthomosaic, atau live stream sample.
- Contoh data minimal 1-3 file untuk testing awal.
- Apakah data memiliki metadata GPS, timestamp, gimbal pitch, altitude, heading, dan speed.
- Apakah kamera menghadap nadir/top-view atau masih oblique.
- Pola terbang yang digunakan, misalnya `top_view_grid` atau `row_scan`.
- Target yang ingin dideteksi: plot kosong, tanaman hilang, tanaman tidak tumbuh, atau area bermasalah lain.
- Apakah sudah ada label/anotasi existing.
- Format output yang diharapkan dari sistem.
- Batasan privasi atau aturan internal perusahaan.
- Apakah data boleh dipakai hanya lokal/offline di laptop.
- Apakah data boleh disimpan di repository atau harus diletakkan di folder lokal yang di-gitignore.

## Parameter Yang Perlu Dicatat

| Parameter | Deskripsi |
| --- | --- |
| `altitude` | Ketinggian drone dari permukaan referensi. |
| `gimbal_pitch` | Sudut pitch gimbal; untuk nadir/top-view gunakan sekitar -90 derajat. |
| `camera_view` | Sudut pandang kamera, misalnya `nadir`, `top_view`, atau `oblique`. |
| `heading` | Arah hadap drone. |
| `speed` | Kecepatan drone saat merekam. |
| `time_of_day` | Waktu pengambilan data. |
| `lighting` | Kondisi cahaya, misalnya cerah, mendung, backlight, atau low light. |
| `flight_pattern` | Pola terbang, misalnya `top_view_grid` atau `row_scan`. |
| `camera_mode` | Mode kamera, resolusi, FPS, dan exposure bila tersedia. |
| `notes_plot_visibility` | Catatan apakah barisan tanaman dan plot kosong terlihat jelas atau tidak. |

Parameter utama dicatat di blok `experiment` pada config agar tersalin otomatis ke `run_manifest.json` dan `run_summary.json`. Nilai ini masih metadata offline/manual, bukan telemetry DJI asli.

## Contoh Tabel Skenario

| Skenario | Gimbal Pitch | Altitude | Speed | Tujuan |
| --- | --- | --- | --- | --- |
| Top-view grid | -90 derajat | Rendah / sedang | Pelan | Melihat pola tanam dan kandidat plot kosong dari atas. |
| Row scan | -90 derajat | Rendah / sedang | Pelan | Mengikuti barisan tanam agar gap antar tanaman mudah diaudit. |
| Variasi altitude | -90 derajat | Berubah | Tetap | Menilai batas detail tanaman terhadap ketinggian. |
| Variasi speed | -90 derajat | Tetap | Berubah | Menilai blur dan stabilitas frame. |
| Orthomosaic review | N/A | N/A | N/A | Menilai apakah `.tif`/orthomosaic perlu tiling sebelum inference. |

## Kriteria Evaluasi

- Pola barisan tanaman terlihat atau tidak.
- Plot kosong terlihat atau tidak.
- Tingkat blur.
- Occlusion oleh daun, bayangan, gulma, atau objek lain.
- Annotation confidence dari reviewer manusia.
- Frame stability.
- Risiko false positive.
- Konsistensi tampilan antar frame.
- Kesesuaian sudut kamera dengan kebutuhan inference.

## Perbandingan Antar Run

Gunakan `run_summary.json` untuk membandingkan eksperimen sudut kamera. Field yang paling berguna untuk tahap awal:

- `mission_id`
- `block_id`
- `target_case`
- `frames_processed`
- `detections_written`
- `confidence_min`, `confidence_max`, `confidence_avg`
- `telemetry.altitude_m`
- `telemetry.gimbal_pitch_deg`
- `telemetry.speed_mps`
- `overlay_enabled`

## Catatan Eksperimen

- Catat kondisi lapangan seobjektif mungkin.
- Jangan mencampur kesimpulan kualitas data dengan akurasi model.
- Simpan video dan output run dengan identitas eksperimen yang jelas.
- GPS drone belum otomatis menunjukkan koordinat objek di tanah.
- Dataset internal tidak boleh dimasukkan ke repository sebelum status izin penyimpanan jelas.
