# Technical Design

## Arsitektur Pipeline Offline

Pipeline offline dirancang sebagai rangkaian modul kecil yang dapat diganti tanpa mengubah kontrak data utama. Fokus desain adalah menjaga batas antara sumber frame, inference, telemetry, output, dan overlay untuk case awal deteksi plot bolong / missing plant pada kebun nanas.

```text
ConfigLoader
-> FrameSource
-> InferenceEngine
-> TelemetryProvider
-> ResultWriter
-> OverlayRenderer opsional
```

## Alur Data End-to-End

1. ConfigLoader membaca konfigurasi lokal.
2. FrameSource membuka video file top-view/nadir dan menghasilkan frame beserta metadata.
3. Frame sampling memilih frame berdasarkan interval.
4. InferenceEngine menghasilkan detection candidate, saat ini label dummy `empty_plot_candidate`.
5. TelemetryProvider menyediakan telemetry untuk timestamp frame.
6. ResultWriter menulis detection ke `JSONL` dan `CSV`.
7. OverlayRenderer membuat output visual bila diaktifkan.
8. Manifest dan summary run disimpan untuk audit eksperimen.

## Struktur Modul

Struktur implementasi awal:

```text
src/drone_plot_gap/
  app.py
  config.py
  frame_source.py
  inference.py
  telemetry.py
  writer.py
  overlay.py
  schema.py
```

Struktur ini menjadi batas modul MVP offline saat ini.

## Interface / Abstraction Layer

### FrameSource

Bertanggung jawab menyediakan frame dan metadata frame. Interface ini memungkinkan migrasi dari file video ke PSDK Liveview tanpa mengubah inference engine.

### InferenceEngine

Bertanggung jawab menerima frame dan menghasilkan daftar detection. Tahap awal memakai dummy inference engine.

### TelemetryProvider

Bertanggung jawab menyediakan telemetry berdasarkan timestamp frame. Tahap awal memakai mock telemetry provider.

### ResultWriter

Bertanggung jawab menulis hasil detection dan metadata ke format output yang stabil.

### OverlayRenderer

Bertanggung jawab membuat visualisasi detection di atas frame. Modul ini opsional dan tidak boleh menjadi syarat utama pipeline.

### ConfigLoader

Bertanggung jawab membaca config lokal dan melakukan validasi minimal terhadap field wajib.

## Rencana Implementasi Awal

- `VideoFileFrameSource`: membaca frame dari file video lokal menggunakan OpenCV.
- `DummyInferenceEngine`: menghasilkan detection dummy atau heuristic sederhana.
- `MockTelemetryProvider`: menghasilkan telemetry lokal berdasarkan timestamp.
- `JsonlCsvResultWriter`: menulis `detections.jsonl`, `detections.csv`, dan metadata run.
- `OpenCvOverlayRenderer`: membuat overlay image atau video untuk validasi visual.
- `run_manifest.json`: menyimpan snapshot config, metadata eksperimen, output, warning, dan summary teknis.
- `run_summary.json`: menyimpan ringkasan kecil untuk membandingkan eksperimen.

## Status Data Input

Input utama saat ini tetap video file lokal. Untuk case plot bolong, video yang paling sesuai adalah top-view/nadir sehingga setiap frame dapat diperlakukan sebagai image dari atas. Dataset publik tidak ditambahkan pada tahap ini. Contoh data asli akan diminta dari pembimbing atau tim GGP/GGF terlebih dahulu.

Setelah contoh data diterima, keputusan teknis berikut baru dievaluasi:

- apakah input utama tetap video, image folder/foto drone, `.tif`/orthomosaic, atau format lain;
- bila input berupa `.tif`/orthomosaic, apakah perlu tiling sebelum inference;
- kebutuhan preprocessing;
- strategi anotasi;
- kebutuhan image folder atau GeoTIFF support;
- apakah model berikutnya deteksi tanaman, deteksi plot kosong, segmentation, atau pendekatan lain berbasis pola barisan.

Sebelum keputusan tersebut dibuat, jangan menambahkan parser dataset publik, auto-download dataset, workflow training, atau integrasi cloud.

## Rencana Migrasi

### Dari VideoFileFrameSource ke PSDKLiveviewFrameSource

FrameSource dibuat sebagai boundary agar sumber frame dapat diganti dari video file ke PSDK Liveview. Metadata frame tetap mempertahankan `frame_index`, `timestamp_ms`, dan `timestamp_iso`. Untuk data orthomosaic, adapter berbeda dapat dibuat di fase berikutnya agar tile `.tif` dapat diproses sebagai frame/image tanpa mengganggu pipeline video MVP.

### Dari MockTelemetryProvider ke PSDKTelemetryProvider

TelemetryProvider dibuat sebagai boundary agar mock telemetry dapat diganti dengan PSDK Data Subscription. Format telemetry tetap mengikuti `DATA_SCHEMA.md`.

### Dari Local Overlay ke DJI Pilot Rendering

Overlay lokal hanya untuk validasi offline. Jika diperlukan, hasil detection dapat dikirim sebagai event atau annotation data untuk rendering di DJI Pilot pada fase target migration.

### Dari Offline App ke Manifold Application / DPK

Offline app menjaga dependency minimal agar lebih mudah dipindahkan ke Manifold Application pada target DJI Manifold 3. DPK packaging baru dirancang setelah pipeline berjalan stabil di runtime target.

## Strategi Error Handling

- Error config: hentikan proses dengan pesan field yang hilang atau invalid.
- Error video input: hentikan proses jika file tidak ditemukan atau tidak dapat dibaca.
- Error per frame: log error dan lanjutkan bila aman.
- Error writer: hentikan proses untuk mencegah output parsial yang tidak jelas.
- Error overlay: log sebagai warning bila output data utama sudah berhasil ditulis.

## Strategi Logging

- Gunakan logging standar Python.
- Level awal: `INFO` untuk progres run, `WARNING` untuk kondisi non-kritis, `ERROR` untuk kegagalan.
- Log harus mencantumkan `run_id`.
- Jangan log credential, path absolut sensitif, atau data rahasia.

## Strategi Output Per Run

Setiap run membuat folder output sendiri:

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

`overlay.mp4` dan `frames/` bersifat opsional sesuai config overlay. `run_id` dapat berbasis timestamp lokal atau UUID pendek. Output lama tidak ditimpa kecuali user menghapusnya secara eksplisit.

Metadata `experiment` berasal dari config lokal dan masih manual/offline. Metadata ini bukan telemetry DJI asli, tetapi dipakai untuk membandingkan variasi sudut kamera, altitude, speed, heading strategy, lighting, dan flight pattern.

Untuk case `missing_plant`, metadata eksperimen default diarahkan ke `camera_view` `nadir`, `gimbal_pitch_deg` `-90.0`, dan `flight_pattern` seperti `top_view_grid` atau `row_scan`.

## Batasan Teknis Yang Harus Dijaga

- Tidak hardcode path absolut.
- Tidak memakai credential, token, cloud, S3, atau database production.
- Tidak masuk PSDK asli sebelum diminta.
- Tidak membuat kontrol drone atau kontrol gimbal.
- Tidak menganggap GPS drone sebagai koordinat objek di tanah.
- Tidak mengunci desain pada dummy inference engine.
- Tidak mengimplementasikan tiling GeoTIFF, training model, atau inference model asli sebelum format dataset lapangan jelas.
- Tidak membuat fitur production sebelum pipeline offline terbukti.
