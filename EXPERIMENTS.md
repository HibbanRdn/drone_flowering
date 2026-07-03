# Flowering Data Experiments

## Tujuan Eksperimen Sudut Kamera

Eksperimen data bertujuan menentukan sudut kamera, altitude, speed, dan kondisi pencahayaan yang paling memungkinkan flowering candidate terlihat jelas pada kebun nanas. Hasil eksperimen dipakai untuk memperbaiki strategi pengambilan data, bukan untuk mengklaim akurasi model final.

Tahap saat ini belum memakai dataset publik. Dataset asli akan diminta dari pembimbing atau tim GGP/GGF terlebih dahulu agar data lebih sesuai dengan kondisi lapangan, komoditas nanas, sudut kamera, dan target operasional.

## Status Dataset

- Belum ada dataset asli lapangan yang masuk ke repository.
- Tidak ada rencana menambahkan dataset publik pada tahap ini.
- Tidak ada auto-download dataset, Roboflow, Kaggle, Mendeley, API key, token, cloud, atau S3.
- Pipeline tetap offline dan lokal sampai pembimbing/tim memberikan contoh data.
- Dukungan image folder, `.tif`/GeoTIFF, preprocessing, anotasi, dan model asli baru diputuskan setelah contoh data diterima.

## Checklist Request Data Ke Pembimbing/Tim

- Jenis data yang tersedia: video, foto/frame, `.tif`, orthomosaic, atau live stream sample.
- Contoh data minimal 1-3 file untuk testing awal.
- Apakah data memiliki metadata GPS, timestamp, gimbal pitch, altitude, heading, dan speed.
- Sudut kamera dan pola terbang yang digunakan.
- Target yang ingin dideteksi: flowering, non-flowering, kondisi tanaman, atau area tertentu.
- Apakah sudah ada label/anotasi existing.
- Format output yang diharapkan dari sistem.
- Batasan privasi atau aturan internal perusahaan.
- Apakah data boleh dipakai hanya lokal/offline di laptop.
- Apakah data boleh disimpan di repository atau harus diletakkan di folder lokal yang di-gitignore.

## Parameter Yang Perlu Dicatat

| Parameter | Deskripsi |
| --- | --- |
| `altitude` | Ketinggian drone dari permukaan referensi. |
| `gimbal_pitch` | Sudut pitch gimbal, misalnya -90, -60, -45, atau -30 derajat. |
| `heading` | Arah hadap drone. |
| `speed` | Kecepatan drone saat merekam. |
| `time_of_day` | Waktu pengambilan data. |
| `lighting` | Kondisi cahaya, misalnya cerah, mendung, backlight, atau low light. |
| `flight_pattern` | Pola terbang, misalnya grid, garis lurus, atau orbit terbatas. |
| `camera_mode` | Mode kamera, resolusi, FPS, dan exposure bila tersedia. |
| `notes_visibility_flowering` | Catatan apakah flowering terlihat jelas atau tidak. |

Parameter utama dicatat di blok `experiment` pada config agar tersalin otomatis ke `run_manifest.json` dan `run_summary.json`. Nilai ini masih metadata offline/manual, bukan telemetry DJI asli.

## Contoh Tabel Skenario

| Skenario | Gimbal Pitch | Altitude | Speed | Tujuan |
| --- | --- | --- | --- | --- |
| Top-down | -90 derajat | Rendah / sedang | Pelan | Melihat pola lahan dan kemungkinan objek dari atas. |
| Oblique 60 | -60 derajat | Rendah / sedang | Pelan | Menilai visibilitas samping tanaman dan flowering. |
| Oblique 45 | -45 derajat | Rendah / sedang | Pelan / sedang | Mencari kompromi antara cakupan dan detail visual. |
| Oblique 30 | -30 derajat | Rendah / sedang | Pelan | Menguji risiko occlusion dan perspektif terlalu miring. |
| Variasi altitude | Sudut tetap | Berubah | Tetap | Menilai batas detail visual terhadap ketinggian. |
| Variasi speed | Sudut tetap | Tetap | Berubah | Menilai blur dan stabilitas frame. |

## Kriteria Evaluasi

- Flowering terlihat atau tidak.
- Tingkat blur.
- Occlusion oleh daun, baris tanaman, atau sudut pandang.
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
- GPS drone belum otomatis menunjukkan koordinat objek flowering di tanah.
- Dataset internal tidak boleh dimasukkan ke repository sebelum status izin penyimpanan jelas.
