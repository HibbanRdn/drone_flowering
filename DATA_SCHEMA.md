# Data Schema

## Schema Version

Versi schema awal:

```text
drone-flowering-detection.v1
```

Semua output detection wajib membawa `schema_version` agar perubahan format dapat dilacak.

## Run Metadata

Field metadata run:

| Field | Wajib | Deskripsi |
| --- | --- | --- |
| `schema_version` | Ya | Versi schema output. |
| `run_id` | Ya | ID unik untuk satu eksekusi pipeline. |
| `created_at_iso` | Ya | Waktu run dibuat dalam format ISO 8601. |
| `config_path` | Tidak | Path config relatif atau path yang diberikan user. |
| `app_version` | Tidak | Versi aplikasi bila tersedia. |
| `notes` | Tidak | Catatan eksperimen. |

## Experiment Metadata

Field `experiment` bersifat opsional di config dan disalin ke `run_manifest.json`.

| Field | Wajib | Deskripsi |
| --- | --- | --- |
| `mission_id` | Tidak | ID eksperimen atau misi. |
| `block_id` | Tidak | ID blok/lokasi kebun. |
| `crop_type` | Tidak | Jenis tanaman, misalnya `pineapple`. |
| `target_case` | Tidak | Target deteksi, misalnya `flowering_candidate`. |
| `flight_pattern` | Tidak | Pola terbang, misalnya `row_following`. |
| `camera_mode` | Tidak | Mode kamera, misalnya `video`. |
| `altitude_m` | Tidak | Altitude rencana/eksperimen dalam meter. |
| `gimbal_pitch_deg` | Tidak | Pitch gimbal rencana/eksperimen. |
| `heading_strategy` | Tidak | Strategi heading, misalnya `along_row`. |
| `speed_mps` | Tidak | Speed rencana/eksperimen dalam meter per detik. |
| `time_of_day` | Tidak | Waktu pengambilan data. |
| `lighting` | Tidak | Kondisi pencahayaan. |
| `notes` | Tidak | Catatan bebas. |

Catatan: metadata eksperimen ini masih offline/manual dan bukan telemetry DJI asli.

## Input Video Metadata

| Field | Wajib | Deskripsi |
| --- | --- | --- |
| `source_video` | Ya | Path input video sesuai config. |
| `fps` | Tidak | FPS video bila dapat dibaca. |
| `width_px` | Tidak | Lebar frame. |
| `height_px` | Tidak | Tinggi frame. |
| `frame_count` | Tidak | Jumlah frame video. |
| `duration_ms` | Tidak | Durasi video dalam milidetik. |

## Frame Metadata

| Field | Wajib | Deskripsi |
| --- | --- | --- |
| `frame_index` | Ya | Index frame pada video. |
| `timestamp_ms` | Ya | Timestamp frame relatif terhadap awal video. |
| `timestamp_iso` | Ya | Timestamp absolut atau estimasi ISO 8601. |
| `sample_index` | Tidak | Urutan frame yang diproses setelah sampling. |

## Detection Result Schema

| Field | Wajib | Deskripsi |
| --- | --- | --- |
| `detection_id` | Ya | ID unik detection dalam satu run. |
| `label` | Ya | Label detection, misalnya `flowering_candidate`. |
| `confidence` | Ya | Nilai confidence 0.0 sampai 1.0. |
| `bbox_xyxy` | Ya | Bounding box `[x_min, y_min, x_max, y_max]`. |
| `bbox_format` | Ya | Nilai tetap `xyxy`. |
| `model_name` | Tidak | Nama engine atau model. |
| `model_version` | Tidak | Versi engine atau model. |

## Telemetry Schema

| Field | Wajib | Deskripsi |
| --- | --- | --- |
| `telemetry.lat` | Ya | Latitude posisi drone. |
| `telemetry.lng` | Ya | Longitude posisi drone. |
| `telemetry.altitude_m` | Ya | Ketinggian drone dalam meter. |
| `telemetry.heading_deg` | Ya | Heading drone dalam derajat. |
| `telemetry.gimbal_pitch_deg` | Ya | Pitch gimbal dalam derajat. |
| `telemetry.speed_mps` | Ya | Kecepatan drone dalam meter per detik. |
| `telemetry.source` | Tidak | Sumber telemetry, misalnya `mock` atau `psdk`. |

Catatan penting: GPS drone belum otomatis sama dengan koordinat objek di tanah. Untuk memperkirakan posisi objek diperlukan model proyeksi kamera, attitude, altitude, kalibrasi kamera, dan asumsi permukaan tanah.

## Kontrak Record Detection Wajib

Setiap detection pada `JSONL` dan `CSV` wajib membawa field berikut dengan tipe dan aturan minimal:

| Field | Tipe | Aturan Minimal |
| --- | --- | --- |
| `schema_version` | string | Harus bernilai `drone-flowering-detection.v1`. |
| `run_id` | string | Tidak kosong dan sama untuk satu run. |
| `source_video` | string | Path input sesuai config, tanpa hardcode path absolut di kode. |
| `frame_index` | integer | Lebih besar atau sama dengan 0. |
| `timestamp_ms` | integer atau float | Lebih besar atau sama dengan 0. |
| `timestamp_iso` | string | Format ISO 8601. |
| `detection_id` | string | Unik dalam satu run. |
| `label` | string | Tidak kosong, contoh `flowering_candidate`. |
| `confidence` | number | Rentang 0.0 sampai 1.0. |
| `bbox_xyxy` | array number | Empat nilai `[x_min, y_min, x_max, y_max]`. |
| `bbox_format` | string | Harus bernilai `xyxy`. |
| `telemetry.lat` | number | Latitude posisi drone. |
| `telemetry.lng` | number | Longitude posisi drone. |
| `telemetry.altitude_m` | number | Ketinggian drone dalam meter. |
| `telemetry.heading_deg` | number | 0.0 sampai kurang dari 360.0 bila tersedia dari sumber. |
| `telemetry.gimbal_pitch_deg` | number | Derajat pitch gimbal. |
| `telemetry.speed_mps` | number | Lebih besar atau sama dengan 0. |

Aturan bounding box:

- `x_min < x_max`.
- `y_min < y_max`.
- Nilai koordinat menggunakan pixel pada frame sumber.
- Koordinat sebaiknya berada dalam ukuran frame. Bila dummy inference sengaja menghasilkan nilai di luar frame untuk pengujian error, record tersebut tidak boleh dipakai sebagai output valid.

## JSONL Output Schema

Setiap baris `detections.jsonl` berisi satu detection:

```json
{
  "schema_version": "drone-flowering-detection.v1",
  "run_id": "20260703-140000",
  "source_video": "data/raw/sample.mp4",
  "frame_index": 120,
  "timestamp_ms": 4000,
  "timestamp_iso": "2026-07-03T14:00:04+07:00",
  "detection_id": "20260703-140000-000001",
  "label": "flowering_candidate",
  "confidence": 0.72,
  "bbox_xyxy": [320, 180, 410, 260],
  "bbox_format": "xyxy",
  "telemetry": {
    "lat": -5.123456,
    "lng": 105.123456,
    "altitude_m": 35.0,
    "heading_deg": 92.5,
    "gimbal_pitch_deg": -60.0,
    "speed_mps": 4.2,
    "source": "mock"
  }
}
```

## CSV Output Columns

Kolom `detections.csv`:

```text
schema_version,run_id,source_video,frame_index,timestamp_ms,timestamp_iso,detection_id,label,confidence,bbox_x_min,bbox_y_min,bbox_x_max,bbox_y_max,bbox_format,telemetry_lat,telemetry_lng,telemetry_altitude_m,telemetry_heading_deg,telemetry_gimbal_pitch_deg,telemetry_speed_mps,telemetry_source
```

Contoh row:

```csv
drone-flowering-detection.v1,20260703-140000,data/raw/sample.mp4,120,4000,2026-07-03T14:00:04+07:00,20260703-140000-000001,flowering_candidate,0.72,320,180,410,260,xyxy,-5.123456,105.123456,35.0,92.5,-60.0,4.2,mock
```

Aturan CSV:

- Satu row merepresentasikan satu detection.
- `bbox_xyxy` diratakan menjadi `bbox_x_min`, `bbox_y_min`, `bbox_x_max`, dan `bbox_y_max`.
- Field telemetry diratakan dengan prefix `telemetry_`.
- Field opsional boleh kosong, tetapi kolom wajib tetap harus ada.
- Gunakan encoding UTF-8 dan pemisah koma.

Jika satu frame tidak memiliki detection, tidak perlu menulis row detection kosong. Informasi run tetap disimpan pada `run_metadata.json` dan `run_manifest.json`.

## Run Manifest Schema

`run_manifest.json` berisi audit lengkap satu run:

```json
{
  "schema_version": "drone-flowering-detection.v1",
  "run_id": "20260703-140000",
  "created_at": "2026-07-03T14:00:00+07:00",
  "source_video": "data/raw/sample.mp4",
  "config_path": "configs/offline.json",
  "config_snapshot": {},
  "experiment": {},
  "outputs": {
    "detections_jsonl": "data/outputs/runs/20260703-140000/detections.jsonl",
    "detections_csv": "data/outputs/runs/20260703-140000/detections.csv",
    "overlay_video": "data/outputs/runs/20260703-140000/overlay.mp4",
    "overlay_frames_dir": "data/outputs/runs/20260703-140000/frames"
  },
  "summary": {
    "frames_processed": 3,
    "detections_written": 3,
    "overlay_enabled": true,
    "overlay_frames_written": 2,
    "started_at": "2026-07-03T14:00:00+07:00",
    "finished_at": "2026-07-03T14:00:01+07:00",
    "duration_seconds": 1.0
  },
  "warnings": []
}
```

`overlay_video` dan `overlay_frames_dir` hanya ada bila output tersebut dibuat.

## Run Summary Schema

`run_summary.json` berisi ringkasan pendek untuk perbandingan eksperimen:

```json
{
  "run_id": "20260703-140000",
  "mission_id": "FLOWERING_TEST_001",
  "block_id": "PG1_005E_F0",
  "target_case": "flowering_candidate",
  "source_video": "data/raw/sample.mp4",
  "frames_processed": 3,
  "detections_written": 3,
  "labels_count": {
    "flowering_candidate": 3
  },
  "confidence_min": 0.72,
  "confidence_max": 0.72,
  "confidence_avg": 0.72,
  "timestamp_ms_min": 0.0,
  "timestamp_ms_max": 2000.0,
  "telemetry": {
    "altitude_m": 35.0,
    "gimbal_pitch_deg": -60.0,
    "speed_mps": 4.2
  },
  "overlay_enabled": true,
  "output_files": {}
}
```

## Field Wajib

- `schema_version`
- `run_id`
- `source_video`
- `frame_index`
- `timestamp_ms`
- `timestamp_iso`
- `detection_id`
- `label`
- `confidence`
- `bbox_xyxy`
- `bbox_format`
- `telemetry.lat`
- `telemetry.lng`
- `telemetry.altitude_m`
- `telemetry.heading_deg`
- `telemetry.gimbal_pitch_deg`
- `telemetry.speed_mps`

## Field Opsional

- `sample_index`
- `model_name`
- `model_version`
- `telemetry.source`
- `run_metadata.notes`
- `input_video_metadata.fps`
- `input_video_metadata.width_px`
- `input_video_metadata.height_px`
- `input_video_metadata.duration_ms`
