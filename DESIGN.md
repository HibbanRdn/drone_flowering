# Technical Design

## Arsitektur Pipeline Offline

Pipeline offline dirancang sebagai rangkaian modul kecil yang dapat diganti tanpa mengubah kontrak data utama. Fokus desain adalah menjaga batas antara sumber frame, inference, telemetry, output, dan overlay.

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
2. FrameSource membuka video file dan menghasilkan frame beserta metadata.
3. Frame sampling memilih frame berdasarkan interval.
4. InferenceEngine menghasilkan detection candidate.
5. TelemetryProvider menyediakan telemetry untuk timestamp frame.
6. ResultWriter menulis detection ke `JSONL` dan `CSV`.
7. OverlayRenderer membuat output visual bila diaktifkan.
8. Metadata run disimpan untuk audit.

## Struktur Modul

Struktur implementasi awal yang disarankan:

```text
src/drone_flowering/
  app.py
  config.py
  frame_source.py
  inference.py
  telemetry.py
  writer.py
  overlay.py
  schema.py
```

Struktur ini belum perlu dibuat sampai dokumen planning disetujui.

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

## Rencana Migrasi

### Dari VideoFileFrameSource ke PSDKLiveviewFrameSource

FrameSource dibuat sebagai boundary agar sumber frame dapat diganti dari video file ke PSDK Liveview. Metadata frame tetap mempertahankan `frame_index`, `timestamp_ms`, dan `timestamp_iso`.

### Dari MockTelemetryProvider ke PSDKTelemetryProvider

TelemetryProvider dibuat sebagai boundary agar mock telemetry dapat diganti dengan PSDK Data Subscription. Format telemetry tetap mengikuti `DATA_SCHEMA.md`.

### Dari Local Overlay ke DJI Pilot Rendering

Overlay lokal hanya untuk validasi offline. Jika diperlukan, hasil detection dapat dikirim sebagai event atau annotation data untuk rendering di DJI Pilot pada fase target migration.

### Dari Offline App ke Manifold Application / DPK

Offline app menjaga dependency minimal agar lebih mudah dipindahkan ke Manifold Application. DPK packaging baru dirancang setelah pipeline berjalan stabil di runtime target.

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
  detections.jsonl
  detections.csv
```

`run_id` dapat berbasis timestamp lokal atau UUID pendek. Output lama tidak ditimpa kecuali user menghapusnya secara eksplisit.

## Batasan Teknis Yang Harus Dijaga

- Tidak hardcode path absolut.
- Tidak memakai credential, token, cloud, S3, atau database production.
- Tidak masuk PSDK asli sebelum diminta.
- Tidak membuat kontrol drone atau kontrol gimbal.
- Tidak menganggap GPS drone sebagai koordinat objek di tanah.
- Tidak mengunci desain pada dummy inference engine.
- Tidak membuat fitur production sebelum pipeline offline terbukti.
