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
- Overlay renderer belum dibuat pada MVP awal.

## Gambaran Pipeline

```text
video file
-> frame source
-> frame sampling
-> inference engine
-> telemetry provider
-> result writer
-> overlay renderer opsional pada fase berikutnya
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
  detections.jsonl
  detections.csv
```

Detail operasional akan dijaga di `RUNBOOK.md`.

## Posisi Terhadap DJI PSDK dan Manifold

Repository ini bukan integrasi DJI final. Prototype ini adalah tahap offline untuk mematangkan pipeline, kontrak data, dan modul internal sebelum migrasi ke PSDK Liveview, Data Subscription, Manifold Application, DPK, dan kemungkinan DJI Pilot rendering.
