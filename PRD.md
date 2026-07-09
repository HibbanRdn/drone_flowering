# Product Requirements Document

## Latar Belakang

Drone AI Project di GGP/GGF membutuhkan fondasi Computer Vision yang dapat membaca video, frame, foto drone, atau data orthomosaic, menjalankan inference, menggabungkan hasil deteksi dengan telemetry, dan menghasilkan output yang dapat diaudit. Drone yang kemungkinan digunakan adalah DJI Matrice 400 dengan DJI Manifold 3. Sebelum masuk ke DJI Manifold 3 atau custom PSDK, diperlukan offline prototype yang dapat dikembangkan dan diuji di laptop.

## Problem Statement

Kebun nanas memiliki pola atau barisan tanam yang dapat diamati dari atas. Pada beberapa area, ada plot yang seharusnya berisi tanaman nanas tetapi kosong atau tanaman tidak tumbuh. Belum tersedia pipeline lokal yang konsisten untuk menguji alur deteksi plot bolong / missing plant dari top-view/nadir video frame, foto drone, atau orthomosaic. Tanpa pipeline offline, risiko debugging akan terlalu besar ketika langsung masuk ke PSDK Liveview, telemetry subscription, Manifold Application, atau DPK.

## Tujuan Project

- Membangun fondasi pipeline offline untuk Computer Vision drone.
- Membuat kontrak data output deteksi dan telemetry.
- Menyediakan struktur yang mudah dimigrasikan ke PSDK Liveview target migration dan Manifold Application target migration.
- Memudahkan audit hasil melalui file `JSONL`, `CSV`, dan overlay opsional.

## Target User dan Audiens

- Peserta KP/magang atau developer yang mengembangkan prototype.
- Tim Digital Innovation yang mengevaluasi kelayakan pipeline.
- Pembimbing teknis yang menilai desain sebelum integrasi DJI.
- Tim lapangan atau agronomi sebagai pengguna hasil eksperimen visual.

## Use Case Utama

Developer menjalankan pipeline pada video drone kebun nanas dengan sudut nadir/top-view. Pipeline mengambil frame sesuai interval, menjalankan dummy inference engine, menggabungkan hasil dengan mock telemetry provider, lalu menghasilkan `JSONL`, `CSV`, dan overlay opsional untuk validasi candidate plot kosong dengan label `empty_plot_candidate`.

## MVP Scope

- Input berupa file video lokal.
- Config lokal untuk path input, interval sampling, dan output.
- Video file frame source.
- Dummy inference engine.
- Mock telemetry provider.
- Result writer untuk `JSONL` dan `CSV`.
- Output folder per run.
- Overlay renderer opsional.
- CLI sederhana.
- Smoke test pipeline end-to-end.

## Non-Goals / Out of Scope

- Dataset publik, auto-download dataset, dan integrasi Roboflow/Kaggle/Mendeley.
- Integrasi DJI PSDK asli.
- PSDK Liveview runtime.
- Data Subscription asli.
- Manifold 3 deployment.
- DPK packaging.
- DJI Pilot rendering.
- Kontrol drone.
- Kontrol gimbal.
- Training model serius.
- Cloud, S3, database production, credential, token, atau secrets.
- Sistem production.

## Input

- File video drone lokal, terutama top-view/nadir.
- Frame atau foto drone top-view pada fase berikutnya bila dibutuhkan.
- `.tif`/orthomosaic pada fase berikutnya bila format data asli membutuhkan tiling.
- File config lokal.
- Parameter sampling frame.
- Mock telemetry atau telemetry log lokal pada fase berikutnya.
- Dataset asli dari pembimbing/tim GGP/GGF belum tersedia dan akan diminta sebelum menentukan format input utama berikutnya.

## Output

- `detections.jsonl` berisi satu record per detection.
- `detections.csv` untuk inspeksi spreadsheet.
- `run_metadata.json` untuk metadata run.
- Folder overlay opsional berisi image atau video hasil anotasi.

## Acceptance Criteria

- Pipeline dapat dijalankan offline dari file video lokal.
- Setiap detection memiliki field wajib sesuai `DATA_SCHEMA.md`.
- Output `JSONL` dan `CSV` dapat dibaca ulang tanpa konteks tambahan.
- Setiap output run tersimpan di folder terpisah.
- Tidak ada path absolut yang di-hardcode.
- Tidak ada credential, token, atau koneksi cloud.
- Modul utama dapat diganti secara bertahap menuju target migration tanpa mengubah kontrak output.

## Risiko Teknis

- Kualitas video/foto tidak cukup untuk membedakan tanaman nanas, tanah kosong, mulsa, bayangan, atau objek lain.
- Orthomosaic `.tif` berukuran besar dan membutuhkan tiling sebelum inference.
- Timestamp frame tidak sinkron dengan telemetry.
- GPS drone tidak otomatis merepresentasikan posisi objek di tanah.
- Dummy inference dapat memberi kesan akurasi yang tidak valid jika tidak diberi label jelas.
- Format output yang berubah-ubah akan menyulitkan migrasi ke PSDK.
- Dependensi berat dapat menyulitkan deployment ke Manifold Application.

## Asumsi Awal

- Video top-view/nadir tersedia sebagai file lokal untuk MVP saat ini.
- Foto/frame drone atau orthomosaic `.tif` mungkin tersedia setelah dataset asli diterima.
- Prototype dijalankan di laptop developer.
- Telemetry awal dapat dimock dengan nilai stabil atau interpolasi sederhana.
- Fokus awal adalah pipeline dan auditability, bukan performa real-time.
- Integrasi DJI baru dilakukan setelah desain offline stabil.
- Dataset publik tidak digunakan saat ini; data lapangan asli dari pembimbing/tim menjadi prioritas sebelum preprocessing, anotasi, training, atau model asli.

## Rencana Pengembangan Menuju Custom PSDK / Manifold 3

1. Stabilkan offline prototype dengan video file frame source untuk top-view/nadir frame.
2. Setelah dataset asli datang, validasi format data top-view: video, image folder, foto drone, atau `.tif`/orthomosaic.
3. Tambahkan dukungan image folder atau GeoTIFF tiling hanya bila dibutuhkan oleh data asli.
4. Evaluasi pendekatan model: deteksi tanaman, deteksi plot kosong, segmentation, atau kombinasi post-processing pola barisan.
5. Tambahkan dukungan telemetry log lokal bila tersedia.
6. Pisahkan interface frame source agar dapat diganti dengan PSDK Liveview.
7. Pisahkan telemetry provider agar dapat diganti dengan PSDK Data Subscription.
8. Uji dependency agar sesuai dengan batasan Manifold Application.
9. Siapkan desain DPK setelah runtime di Manifold terbukti berjalan.
10. Evaluasi DJI Pilot rendering setelah format event dan kebutuhan visual jelas.
