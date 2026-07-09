# Drone Missing Plant Offline Prototype

## Ringkasan Project

Project ini adalah offline prototype untuk pipeline Computer Vision drone pada konteks Digital Innovation / Drone AI Project di GGP/GGF. Prototype berfokus pada pembacaan video atau frame drone, pengambilan frame, inference awal, penggabungan hasil deteksi dengan telemetry, dan penulisan output yang dapat diaudit.

Case awal yang diarahkan saat ini adalah deteksi plot bolong / missing plant pada kebun nanas. Plot bolong adalah area atau titik tanam yang seharusnya berisi tanaman nanas, tetapi kosong atau tanaman tidak tumbuh. Karena case ini berbasis pola tanaman dari atas, pendekatan awal diarahkan ke top-view/nadir frame, foto drone, atau orthomosaic `.tif`, bukan oblique side-view.

Drone yang kemungkinan digunakan adalah DJI Matrice 400 dengan DJI Manifold 3. Tahap awal belum menargetkan akurasi model tinggi, tetapi memastikan pipeline data tersusun rapi sebelum diarahkan ke custom PSDK, PSDK Liveview, telemetry subscription, dan Manifold Application.

## Current Status

Folder project lokal saat ini:

```text
/Users/muhamadhibbanramadhan/Documents/drone_plot_gap
```

Package Python dan command utama menggunakan nama `drone_plot_gap`. Project masih berada pada tahap offline prototype di laptop. Pipeline yang sudah tersedia mencakup video file input, frame sampling, dummy inference, mock telemetry, output `JSONL`/`CSV`, run manifest, run summary, overlay lokal, dan smoke test.

## First Case: Plot Gap / Missing Plant

First case resmi adalah deteksi plot bolong / missing plant pada kebun nanas. Input utama yang diantisipasi adalah top-view/nadir video frame, foto drone, atau orthomosaic `.tif`.

Target metadata default:

- `target_case`: `missing_plant`
- `crop_type`: `pineapple`
- `camera_view`: `nadir`
- `gimbal_pitch_deg`: `-90.0`
- `flight_pattern`: `top_view_grid`
- dummy label: `empty_plot_candidate`

## Relationship with DJI Payload-SDK

DJI Payload-SDK resmi sudah tersedia secara lokal di:

```text
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master
```

DJI Developer App untuk Payload SDK - Manifold 3 sudah dibuat, tetapi credential tidak boleh ditulis di repository. File app info Manifold 3 yang relevan berada di sample C dan C++ Payload-SDK:

```text
samples/sample_c/platform/linux/manifold3/application/dji_sdk_app_info.h
samples/sample_c++/platform/linux/manifold3/application/dji_sdk_app_info.h
```

Sample resmi PSDK harus berhasil berjalan terlebih dahulu sebelum membuat custom app untuk deteksi plot bolong. Catatan detail ada di `PSDK_INTEGRATION_NOTES.md`.

## Tujuan Prototype

- Membuktikan alur data Computer Vision secara offline di laptop.
- Menentukan kontrak data hasil deteksi dan telemetry.
- Menghasilkan output `JSONL` dan `CSV` yang mudah diperiksa ulang.
- Menyediakan fondasi migrasi bertahap ke PSDK Liveview target migration dan Manifold Application target migration.
- Menyiapkan konteks eksperimen untuk `target_case` `missing_plant` dengan label dummy `empty_plot_candidate`.

## Scope Tahap Awal

- Membaca video dari file lokal.
- Melakukan frame sampling.
- Menjalankan dummy inference engine deterministik.
- Menggabungkan hasil inference dengan mock telemetry provider.
- Menulis hasil ke result writer berbasis `JSONL` dan `CSV`.
- Membuat overlay renderer lokal opsional untuk audit visual.

## Gambaran Pipeline

```text
video file / top-view frame
-> frame source
-> frame sampling
-> inference engine
-> telemetry provider
-> result writer
-> overlay renderer opsional
```

## Not Yet Implemented

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

Tahap berikutnya adalah meminta dan menunggu dataset asli dari pembimbing atau tim GGP/GGF. Data yang paling relevan untuk case plot bolong kemungkinan berupa video nadir/top-view, frame atau foto drone dari atas, atau `.tif`/orthomosaic kebun nanas.

Jika input berupa video, frame dapat diproses sebagai top-view image. Jika input berupa `.tif`/orthomosaic, tahap berikutnya kemungkinan membutuhkan tiling sebelum inference. Keputusan format input utama, kebutuhan preprocessing, strategi anotasi, dukungan image folder/GeoTIFF, dan pilihan pendekatan model seperti deteksi tanaman, deteksi plot kosong, segmentation, atau pendekatan lain baru ditentukan setelah contoh data asli diterima.

Catatan penting: GPS drone belum otomatis sama dengan koordinat objek di tanah. Estimasi posisi objek membutuhkan model proyeksi kamera, attitude, altitude, kalibrasi kamera, dan asumsi permukaan tanah.

## Rencana Cara Menjalankan App

Siapkan environment lokal:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Ubah `configs/offline.json` agar `input.video_path` mengarah ke video lokal yang tersedia, lalu jalankan:

```bash
.venv/bin/python -m drone_plot_gap --config configs/offline.json
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

`run_manifest.json` menyimpan snapshot config, metadata eksperimen, daftar output, warning, dan ringkasan teknis run. `run_summary.json` menyimpan ringkasan kecil untuk membandingkan eksperimen top-view, misalnya mission, block, target case, jumlah detection, confidence, telemetry mock, dan status overlay.

## Manual Check Command

Jalankan dari root project:

```bash
pwd
git status --short
.venv/bin/python -m compileall -q src tests
.venv/bin/python tests/test_pipeline_smoke.py
.venv/bin/python -m drone_plot_gap --config configs/offline.json
git diff --check
```

Command default config boleh menghasilkan error informatif bila `data/raw/sample.mp4` belum tersedia.

## Posisi Terhadap DJI PSDK dan Manifold

Repository ini bukan integrasi DJI final. Prototype ini adalah tahap offline untuk mematangkan pipeline, kontrak data, dan modul internal sebelum migrasi ke PSDK Liveview, Data Subscription, Manifold Application, DPK, dan kemungkinan DJI Pilot rendering.
