# Drone Flowering Offline Prototype

## Ringkasan Project

Project ini adalah offline prototype untuk pipeline Computer Vision drone pada konteks Digital Innovation / Drone AI Project di GGP/GGF. Prototype berfokus pada pembacaan video drone, pengambilan frame, inference awal, penggabungan hasil deteksi dengan telemetry, dan penulisan output yang dapat diaudit.

Case awal adalah deteksi flowering candidate atau kondisi tanaman pada kebun nanas dari video drone dengan sudut kamera tertentu. Tahap awal belum menargetkan akurasi model tinggi, tetapi memastikan pipeline data tersusun rapi sebelum diarahkan ke custom PSDK dan DJI Manifold 3.

## Tujuan Prototype

- Membuktikan alur data Computer Vision secara offline di laptop.
- Menentukan kontrak data hasil deteksi dan telemetry.
- Menghasilkan output `JSONL` dan `CSV` yang mudah diperiksa ulang.
- Menyediakan fondasi migrasi bertahap ke PSDK Liveview target migration dan Manifold Application target migration.

## Scope Tahap Awal

- Membaca video dari file lokal.
- Melakukan frame sampling.
- Menjalankan dummy inference engine deterministik.
- Menggabungkan hasil inference dengan mock telemetry provider.
- Menulis hasil ke result writer berbasis `JSONL` dan `CSV`.
- Membuat overlay renderer lokal opsional untuk audit visual.

## Gambaran Pipeline

```text
video file
-> frame source
-> frame sampling
-> inference engine
-> telemetry provider
-> result writer
-> overlay renderer opsional
```

## Batasan Yang Belum Dikerjakan

- Belum ada integrasi DJI PSDK asli.
- Belum ada deployment ke Manifold 3.
- Belum ada DPK packaging.
- Belum ada DJI Pilot rendering.
- Belum ada kontrol drone atau kontrol gimbal.
- Belum ada training model serius.
- Belum ada cloud, S3, database production, credential, token, atau secrets.
- Belum ada fitur production.
- Belum ada dataset asli lapangan dari pembimbing/tim GGP/GGF.
- Tidak menambahkan dataset publik, auto-download dataset, atau integrasi Roboflow/Kaggle/Mendeley pada tahap ini.
- Belum ada model AI asli, preprocessing dataset, atau workflow anotasi.

## Status Dataset

Tahap berikutnya adalah meminta dan menunggu dataset asli dari pembimbing atau tim GGP/GGF. Data yang mungkin diterima dapat berupa video drone, frame/foto drone, `.tif`/orthomosaic, live stream sample, atau data lain terkait flowering/kondisi tanaman nanas.

Keputusan format input utama, kebutuhan preprocessing, strategi anotasi, dukungan image folder/GeoTIFF, dan pilihan pendekatan model seperti object detection, segmentation, atau pendekatan lain baru ditentukan setelah contoh data asli diterima.

## Rencana Cara Menjalankan App

Siapkan environment lokal:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Ubah `configs/offline.json` agar `input.video_path` mengarah ke video lokal yang tersedia, lalu jalankan:

```bash
python -m drone_flowering --config configs/offline.json
```

Output setiap run berada pada folder terpisah, misalnya:

```text
data/outputs/runs/<run_id>/
  run_metadata.json
  run_manifest.json
  run_summary.json
  detections.jsonl
  detections.csv
  overlay.mp4        # jika overlay.output_video aktif
  frames/            # jika overlay.output_frames aktif
```

Detail operasional akan dijaga di `RUNBOOK.md`.

Status development saat ini dan panduan demo/manual check tersedia di `DEV_STATUS.md`.

`run_manifest.json` menyimpan snapshot config, metadata eksperimen, daftar output, warning, dan ringkasan teknis run. `run_summary.json` menyimpan ringkasan kecil untuk membandingkan eksperimen sudut kamera, misalnya mission, block, jumlah detection, confidence, telemetry mock, dan status overlay.

## Posisi Terhadap DJI PSDK dan Manifold

Repository ini bukan integrasi DJI final. Prototype ini adalah tahap offline untuk mematangkan pipeline, kontrak data, dan modul internal sebelum migrasi ke PSDK Liveview, Data Subscription, Manifold Application, DPK, dan kemungkinan DJI Pilot rendering.
