# Status Development dan Panduan Demo

## 1. Ringkasan Status Project Saat Ini

Project `drone_plot_gap` saat ini berada pada tahap offline prototype untuk pipeline Computer Vision drone dalam konteks Drone AI Project GGP/GGF. Fokus case terbaru adalah deteksi plot bolong / missing plant pada kebun nanas, dengan target data top-view/nadir dari video, foto drone, atau orthomosaic. Prototype ini sudah membuktikan alur data dasar:

```text
video file -> frame sampling -> dummy inference -> mock telemetry -> JSONL/CSV -> run summary/manifest -> overlay visual
```

Tahap ini belum bertujuan menghasilkan deteksi missing plant yang akurat. Fokus utamanya adalah memastikan boundary pipeline, kontrak data, output audit, dan cara demo offline sudah dapat berjalan di laptop sebelum ada sample dataset asli dari pembimbing atau tim.

Folder project lokal saat ini adalah:

```text
/Users/muhamadhibbanramadhan/Documents/drone_plot_gap
```

Command utama saat ini:

```bash
.venv/bin/python -m drone_plot_gap --config configs/offline.json
```

DJI Payload-SDK resmi sudah tersedia di `/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master` dan sudah diinspeksi secara read-only. PSDK masih menjadi target migrasi desain; belum ada integrasi DJI asli di project ini.

## 2. Fitur Yang Sudah Selesai

Fitur MVP offline yang sudah tersedia:

- Config loader untuk membaca config lokal dari `configs/offline.json`.
- Video input dari file lokal.
- Frame sampling berdasarkan interval frame.
- Dummy inference deterministik untuk menghasilkan candidate detection terstruktur.
- Mock telemetry untuk melengkapi detection dengan telemetry simulasi.
- JSONL writer untuk output audit per detection.
- CSV writer untuk output tabular yang mudah dibuka di spreadsheet.
- Output folder per run di `data/outputs/runs/<run_id>/`.
- Run manifest melalui `run_manifest.json`.
- Run summary melalui `run_summary.json`.
- Overlay video/frame lokal untuk audit visual bila opsi overlay diaktifkan.
- Smoke test untuk memeriksa alur end-to-end secara kecil.

## 3. Fitur Yang Sengaja Belum Dibuat

Fitur berikut belum dibuat karena memang di luar scope tahap awal:

- Model AI asli.
- Training model.
- Dataset publik.
- DJI PSDK.
- Manifold 3 deployment.
- DPK packaging.
- DJI Pilot rendering.
- Flight control.
- Gimbal control.
- Cloud, S3, database, atau integrasi production.

Catatan PSDK:

- DJI Developer App untuk Payload SDK - Manifold 3 sudah dibuat.
- App ID, App Key, App License, App Advanced License, dan developer account tidak boleh ditulis di repository atau dokumentasi.
- Sample PSDK resmi harus berhasil berjalan terlebih dahulu sebelum custom app plot bolong dibuat.
- Detail mapping dan urutan kerja tersedia di `PSDK_INTEGRATION_NOTES.md`.

Pembatasan ini menjaga prototype tetap kecil, offline, dan mudah divalidasi sampai format data lapangan asli sudah jelas.

## 4. Cara Manual Check Di Laptop

Jalankan command berikut dari root repository:

```bash
pwd
ls -la
git status --short
```

Cek syntax Python:

```bash
.venv/bin/python -m compileall -q src tests
```

Jalankan smoke test:

```bash
.venv/bin/python tests/test_pipeline_smoke.py
```

Jalankan pipeline dengan config default:

```bash
.venv/bin/python -m drone_plot_gap --config configs/offline.json
```

Catatan: command pipeline dengan config default kemungkinan akan error bila `data/raw/sample.mp4` belum ada. Error seperti itu normal selama sample video asli belum tersedia atau path video belum diubah.

## 5. Cara Menjalankan Demo Dengan Sample Video Lokal

Ada dua pilihan untuk menyiapkan input demo:

- Letakkan sample video di `data/raw/sample.mp4`.
- Atau ubah nilai `input.video_path` di `configs/offline.json` agar mengarah ke video lokal yang tersedia.

Setelah input siap, jalankan:

```bash
.venv/bin/python -m drone_plot_gap --config configs/offline.json
```

Output yang diharapkan berada pada folder run terbaru:

```text
data/outputs/runs/<run_id>/detections.jsonl
data/outputs/runs/<run_id>/detections.csv
data/outputs/runs/<run_id>/run_manifest.json
data/outputs/runs/<run_id>/run_summary.json
data/outputs/runs/<run_id>/overlay.mp4
data/outputs/runs/<run_id>/frames/
```

`overlay.mp4` hanya dibuat jika `overlay.enabled` dan `overlay.output_video` aktif. Folder `frames/` hanya dibuat jika `overlay.enabled` dan `overlay.output_frames` aktif.

## 6. Cara Mengecek Output Manual

Lihat beberapa folder run terbaru:

```bash
find data/outputs/runs -maxdepth 1 -type d | sort | tail -n 5
```

Jika sudah tahu `run_id`, cek isi folder dan output utama:

```bash
ls -la data/outputs/runs/<run_id>
head -n 3 data/outputs/runs/<run_id>/detections.jsonl
column -s, -t < data/outputs/runs/<run_id>/detections.csv | head
cat data/outputs/runs/<run_id>/run_summary.json
cat data/outputs/runs/<run_id>/run_manifest.json
```

Untuk membuka overlay:

```bash
open data/outputs/runs/<run_id>/overlay.mp4
open data/outputs/runs/<run_id>/frames
```

Jika overlay belum aktif, file `overlay.mp4` atau folder `frames/` bisa tidak ada. Kondisi tersebut normal dan mengikuti konfigurasi `overlay` pada `configs/offline.json`.

## 7. Narasi Singkat Untuk Demo Ke Pembimbing

Prototype ini belum ditujukan untuk mendeteksi missing plant secara akurat. Tujuan tahap ini adalah membangun pipeline data Computer Vision yang rapi dan dapat diaudit dari video drone lokal sampai menjadi output terstruktur. Case terbaru diarahkan ke top-view/nadir karena plot bolong lebih mudah dianalisis dari pola barisan tanaman. Pada tahap berikutnya, input video file dapat diganti arahnya menjadi PSDK Liveview, dummy inference dapat diganti dengan model Computer Vision asli, dan mock telemetry dapat diganti dengan DJI telemetry subscription. Overlay lokal yang tersedia sekarang berfungsi untuk audit visual di laptop, sebelum nanti arah desainnya dapat dikaji untuk rendering lain seperti DJI Pilot sesuai kebutuhan tahap berikutnya.

## 8. Checklist Demo Ke Pembimbing

- Jalankan smoke test.
- Tunjukkan `configs/offline.json`.
- Jalankan pipeline dengan video sample.
- Tunjukkan folder output run.
- Buka `detections.jsonl`.
- Buka `detections.csv`.
- Buka `run_summary.json`.
- Buka `run_manifest.json`.
- Buka overlay video atau folder frame bila overlay diaktifkan.
- Jelaskan batasan tahap saat ini dan next step menunggu dataset asli.

## 9. Pertanyaan Untuk Pembimbing Setelah Demo

- Dataset asli tersedia dalam bentuk apa: video, foto, `.tif`, orthomosaic, atau format lain?
- Apakah ada metadata GPS, timestamp, gimbal pitch, altitude, heading, atau speed?
- Apakah data diambil dari sudut nadir/top-view dengan gimbal sekitar -90 derajat?
- Pola terbang yang direncanakan apakah `top_view_grid`, `row_scan`, atau pola lain?
- Definisi operasional plot bolong/missing plant yang ingin dideteksi seperti apa?
- Apakah ada label atau anotasi existing?
- Output yang diharapkan apakah bounding box, CSV, JSON, peta, report, atau kombinasi beberapa format?
- Apakah hasil perlu real-time di drone atau cukup near real-time setelah penerbangan?
- Apakah data boleh diproses lokal di laptop saya?

## 10. Status Teknis Singkat Untuk Pembimbing

Saat ini saya sudah menyiapkan offline prototype pipeline Computer Vision untuk Drone AI Project GGP/GGF dengan konteks terbaru deteksi plot bolong / missing plant pada kebun nanas. Pipeline sudah bisa membaca video file lokal, melakukan frame sampling, menjalankan dummy inference deterministik dengan label `empty_plot_candidate`, menambahkan mock telemetry, menulis output `JSONL` dan `CSV`, membuat folder output per run, serta menghasilkan `run_manifest.json`, `run_summary.json`, dan overlay lokal untuk audit visual. Tahap ini belum memakai model AI asli, training, DJI PSDK, Manifold 3 deployment, DPK, cloud, atau kontrol drone/gimbal. Next step utama adalah menunggu sample dataset asli top-view/nadir agar format input, kebutuhan metadata, strategi anotasi, dan arah model dapat ditentukan dengan tepat.
