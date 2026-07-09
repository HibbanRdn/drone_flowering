# Runbook Offline Prototype

## Cara Setup Environment

Environment lokal menggunakan Python dan dependency minimal untuk MVP offline.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Dependency runtime utama adalah OpenCV headless untuk membaca video lokal.

## Cara Menyiapkan Config

Config awal direncanakan berada di:

```text
configs/offline.json
```

Config minimal akan mencakup:

- path video input;
- folder output;
- metadata eksperimen;
- interval sampling frame;
- parameter mock telemetry;
- opsi overlay lokal.

Untuk MVP awal, config harus memakai path relatif. Default `input.video_path` adalah `data/raw/sample.mp4`; ubah nilai ini ke video lokal yang tersedia sebelum menjalankan pipeline.

Metadata eksperimen bersifat opsional dan masih diisi manual/offline, bukan telemetry DJI asli:

```json
{
  "experiment": {
    "mission_id": "MISSING_PLANT_TEST_001",
    "block_id": "PINEAPPLE_BLOCK_001",
    "crop_type": "pineapple",
    "target_case": "missing_plant",
    "flight_pattern": "top_view_grid",
    "camera_view": "nadir",
    "camera_mode": "video",
    "altitude_m": 35.0,
    "gimbal_pitch_deg": -90.0,
    "heading_strategy": "along_row",
    "speed_mps": 2.0,
    "time_of_day": "morning",
    "lighting": "unknown",
    "notes": "offline prototype run"
  }
}
```

## Status Dataset

Dataset publik tidak digunakan pada tahap ini. Jangan menambahkan auto-download dataset, integrasi Roboflow, Kaggle, Mendeley, API key, token, credential, cloud, atau S3.

Data asli akan diminta dari pembimbing atau tim GGP/GGF. Untuk case plot bolong / missing plant, data yang paling relevan adalah top-view/nadir video frame, foto drone dari atas, atau orthomosaic `.tif`. Sampai data tersebut diterima, pipeline tetap memakai input video file lokal dan dummy inference. Jangan menambah dukungan image folder, GeoTIFF tiling, preprocessing besar, anotasi, training, atau model inference asli sebelum format data lapangan jelas.

Jika input berupa video, frame dapat diproses sebagai top-view image. Jika input berupa `.tif`/orthomosaic, tahap berikutnya perlu mengevaluasi tiling sebelum inference karena file biasanya besar dan memiliki koordinat spasial sendiri.

## Catatan PSDK / Manifold 3

Project ini belum memiliki integrasi DJI PSDK asli. DJI Payload-SDK resmi sudah tersedia secara lokal di `/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master` dan digunakan sebagai referensi target migrasi desain.

Catatan operasional PSDK, file app info Manifold 3, sample FC subscription, sample liveview, tool DPK, aturan credential, dan urutan kerja saat Manifold 3 datang tersedia di `PSDK_INTEGRATION_NOTES.md`.

Jangan menulis App ID, App Key, App License, App Advanced License, developer account, atau credential DJI lain di dokumentasi, source code, commit, atau GitHub.

## Checklist Request Data

Gunakan checklist berikut saat meminta data ke pembimbing/tim:

- Jenis data yang tersedia: video, foto/frame, `.tif`, orthomosaic, atau live stream sample.
- Contoh data minimal 1-3 file untuk testing awal.
- Ketersediaan metadata GPS, timestamp, gimbal pitch, altitude, heading, dan speed.
- Apakah kamera menghadap nadir/top-view atau oblique.
- Pola terbang yang digunakan, misalnya `top_view_grid` atau `row_scan`.
- Target yang ingin dideteksi: plot kosong, missing plant, tanaman tidak tumbuh, atau area bermasalah lain.
- Ada atau tidaknya label/anotasi existing.
- Format output yang diharapkan dari sistem.
- Batasan privasi atau aturan internal perusahaan.
- Apakah data boleh dipakai hanya lokal/offline di laptop.
- Apakah data boleh disimpan di repository atau harus diletakkan di folder lokal yang di-gitignore.

Opsi overlay tersedia di blok `overlay`:

```json
{
  "overlay": {
    "enabled": false,
    "output_video": true,
    "output_frames": false,
    "max_frames": 100
  }
}
```

## Cara Menjalankan Pipeline

Perintah utama:

```bash
.venv/bin/python -m drone_plot_gap --config configs/offline.json
```

Pipeline akan membaca video lokal, melakukan frame sampling, menjalankan inference engine, mengambil telemetry dari telemetry provider, lalu menulis output melalui result writer. Pada konteks baru, setiap frame video diasumsikan sebagai top-view image bila data diambil dengan `camera_view` `nadir`.

Jika video tidak tersedia, CLI akan berhenti dengan pesan seperti:

```text
ERROR: Video input tidak ditemukan: data/raw/sample.mp4
```

## Lokasi Output

Output setiap run direncanakan tersimpan di:

```text
data/outputs/runs/<run_id>/
  run_metadata.json
  run_manifest.json
  run_summary.json
  detections.jsonl
  detections.csv
  overlay.mp4
  frames/
```

`overlay.mp4` hanya dibuat bila `overlay.enabled` dan `overlay.output_video` bernilai `true`. Folder `frames/` hanya dibuat bila `overlay.enabled` dan `overlay.output_frames` bernilai `true`.

`run_manifest.json` adalah catatan audit lengkap untuk satu run: snapshot config, metadata eksperimen, daftar output, warning, dan summary teknis. `run_summary.json` adalah ringkasan pendek untuk membandingkan eksperimen top-view/nadir antar video.

## Cara Membaca JSONL / CSV

`detections.jsonl` berisi satu JSON object per baris. Format ini cocok untuk proses streaming, audit per detection, dan migrasi ke event pipeline.

`detections.csv` berisi field yang diratakan agar mudah dibuka di spreadsheet. Kolom CSV mengikuti kontrak di `DATA_SCHEMA.md`.

Untuk membandingkan eksperimen, buka `run_summary.json` dari beberapa run dan bandingkan `mission_id`, `block_id`, `target_case`, `frames_processed`, `detections_written`, confidence, `altitude_m`, `gimbal_pitch_deg`, `speed_mps`, dan status overlay.

Catatan penting: GPS drone belum otomatis sama dengan koordinat objek di tanah. Koordinat objek plot kosong baru dapat diperkirakan bila tersedia model proyeksi kamera, attitude, altitude, kalibrasi kamera, dan asumsi permukaan tanah.

## Debug Error Umum

| Masalah | Kemungkinan Penyebab | Tindakan |
| --- | --- | --- |
| Config tidak terbaca | Path config salah atau field wajib hilang | Periksa path dan isi config. |
| Video tidak terbuka | Path video salah atau codec tidak didukung | Pastikan file ada dan dapat diputar lokal. |
| Output tidak dibuat | Folder output tidak dapat ditulis | Periksa permission folder output. |
| Detection kosong | Dummy inference tidak menghasilkan candidate pada frame | Periksa konfigurasi dummy inference dan sampling. |
| Telemetry kosong | Mock telemetry belum dikonfigurasi | Periksa parameter telemetry pada config. |
| Overlay tidak dibuat | `overlay.enabled` masih `false` atau output overlay dimatikan | Periksa blok `overlay` pada config. |
| Summary tidak sesuai | Config eksperimen atau sampling tidak sesuai run | Periksa `run_manifest.json` dan `run_summary.json`. |

## Cara Membersihkan Output Eksperimen

Output eksperimen dapat dihapus secara manual dari folder:

```text
data/outputs/
```

Jangan hapus output yang masih diperlukan untuk audit atau perbandingan eksperimen. Untuk eksperimen penting, arsipkan `run_manifest.json`, `run_summary.json`, `detections.jsonl`, `detections.csv`, overlay, dan catatan eksperimen terkait.
