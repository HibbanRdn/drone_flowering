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
- interval sampling frame;
- parameter mock telemetry.

Untuk MVP awal, config harus memakai path relatif. Default `input.video_path` adalah `data/raw/sample.mp4`; ubah nilai ini ke video lokal yang tersedia sebelum menjalankan pipeline.

## Cara Menjalankan Pipeline

Perintah utama:

```bash
python -m drone_flowering --config configs/offline.json
```

Pipeline akan membaca video lokal, melakukan frame sampling, menjalankan inference engine, mengambil telemetry dari telemetry provider, lalu menulis output melalui result writer.

Jika video tidak tersedia, CLI akan berhenti dengan pesan seperti:

```text
ERROR: Video input tidak ditemukan: data/raw/sample.mp4
```

## Lokasi Output

Output setiap run direncanakan tersimpan di:

```text
data/outputs/runs/<run_id>/
  run_metadata.json
  detections.jsonl
  detections.csv
```

Overlay belum dibuat pada MVP awal.

## Cara Membaca JSONL / CSV

`detections.jsonl` berisi satu JSON object per baris. Format ini cocok untuk proses streaming, audit per detection, dan migrasi ke event pipeline.

`detections.csv` berisi field yang diratakan agar mudah dibuka di spreadsheet. Kolom CSV mengikuti kontrak di `DATA_SCHEMA.md`.

## Debug Error Umum

| Masalah | Kemungkinan Penyebab | Tindakan |
| --- | --- | --- |
| Config tidak terbaca | Path config salah atau field wajib hilang | Periksa path dan isi config. |
| Video tidak terbuka | Path video salah atau codec tidak didukung | Pastikan file ada dan dapat diputar lokal. |
| Output tidak dibuat | Folder output tidak dapat ditulis | Periksa permission folder output. |
| Detection kosong | Dummy inference tidak menghasilkan candidate pada frame | Periksa konfigurasi dummy inference dan sampling. |
| Telemetry kosong | Mock telemetry belum dikonfigurasi | Periksa parameter telemetry pada config. |

## Cara Membersihkan Output Eksperimen

Output eksperimen dapat dihapus secara manual dari folder:

```text
data/outputs/
```

Jangan hapus output yang masih diperlukan untuk audit atau perbandingan eksperimen. Untuk eksperimen penting, arsipkan `run_metadata.json`, `detections.jsonl`, `detections.csv`, dan catatan eksperimen terkait.
