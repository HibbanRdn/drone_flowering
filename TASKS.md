# Implementation Tasks

## Checklist Fase

- [x] Fase 0: Setup repository dan dependency minimal
  - Tujuan: menyiapkan struktur dasar repository dan dependency paling kecil untuk offline prototype.
  - File kemungkinan dibuat/diubah: `pyproject.toml`, `README.md`, `.gitignore`.
  - Acceptance criteria: environment lokal dapat dibuat, dependency inti tercatat, tidak ada dependency DJI atau cloud.
  - Catatan batasan: jangan membuat integrasi PSDK, DPK, credential, atau fitur production.

- [x] Fase 1: Config loader
  - Tujuan: membaca config lokal untuk input video, output folder, sampling, dan mock telemetry.
  - File kemungkinan dibuat/diubah: `configs/offline.json`, `src/drone_flowering/config.py`.
  - Acceptance criteria: config valid dapat dibaca; field wajib yang hilang menghasilkan error jelas.
  - Catatan batasan: jangan hardcode path absolut.

- [x] Fase 2: Video reader / frame source
  - Tujuan: membuat `VideoFileFrameSource` untuk membaca frame dari file video lokal.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/frame_source.py`.
  - Acceptance criteria: frame dan metadata dasar dapat dihasilkan dari video.
  - Catatan batasan: belum membuat PSDK Liveview frame source.

- [x] Fase 3: Frame sampling
  - Tujuan: memilih frame berdasarkan interval frame atau interval waktu.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/frame_source.py`, `src/drone_flowering/app.py`.
  - Acceptance criteria: jumlah frame yang diproses sesuai config sampling.
  - Catatan batasan: cukup satu strategi sampling sederhana untuk MVP.

- [x] Fase 4: Dummy inference
  - Tujuan: membuat `DummyInferenceEngine` untuk menghasilkan detection terstruktur.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/inference.py`.
  - Acceptance criteria: output detection mengikuti `DATA_SCHEMA.md`.
  - Catatan batasan: jangan training model serius.

- [x] Fase 5: Mock telemetry
  - Tujuan: membuat `MockTelemetryProvider` untuk menyediakan telemetry per frame.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/telemetry.py`.
  - Acceptance criteria: setiap detection memiliki telemetry wajib.
  - Catatan batasan: jangan mengklaim GPS drone sebagai koordinat objek di tanah.

- [x] Fase 6: Result writer JSONL / CSV
  - Tujuan: membuat `JsonlCsvResultWriter`.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/writer.py`, `src/drone_flowering/schema.py`.
  - Acceptance criteria: `detections.jsonl` dan `detections.csv` valid dan mengikuti schema.
  - Catatan batasan: writer harus gagal jelas bila output tidak dapat ditulis.

- [x] Fase 7: Output folder per run
  - Tujuan: memastikan setiap eksekusi memiliki folder output sendiri.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/app.py`, `src/drone_flowering/writer.py`.
  - Acceptance criteria: output tersimpan di `data/outputs/runs/<run_id>/` tanpa menimpa run lain.
  - Catatan batasan: jangan menghapus output lama secara otomatis.

- [ ] Fase 8: Overlay image / video
  - Tujuan: membuat `OpenCvOverlayRenderer` opsional untuk validasi visual.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/overlay.py`.
  - Acceptance criteria: overlay dapat dibuat bila opsi aktif; pipeline data tetap berjalan bila overlay nonaktif.
  - Catatan batasan: overlay bukan pengganti output `JSONL` atau `CSV`.

- [x] Fase 9: CLI sederhana
  - Tujuan: menyediakan perintah menjalankan pipeline dengan config.
  - File kemungkinan dibuat/diubah: `src/drone_flowering/app.py`, `src/drone_flowering/__main__.py`.
  - Acceptance criteria: app dapat dijalankan dengan `python -m drone_flowering --config configs/offline.json`.
  - Catatan batasan: jangan membuat CLI kompleks sebelum diperlukan.

- [x] Fase 10: Smoke test
  - Tujuan: membuat pengecekan kecil untuk alur end-to-end.
  - File kemungkinan dibuat/diubah: `tests/test_pipeline_smoke.py`.
  - Acceptance criteria: smoke test memverifikasi output utama dibuat dan field wajib tersedia.
  - Catatan batasan: cukup test kecil; jangan membuat test suite besar sebelum logic stabil.

- [x] Fase 11: Dokumentasi runbook
  - Tujuan: memperbarui panduan operasional sesuai implementasi aktual.
  - File kemungkinan dibuat/diubah: `RUNBOOK.md`, `README.md`.
  - Acceptance criteria: user dapat setup, menjalankan, membaca output, dan debug error umum.
  - Catatan batasan: jangan mendokumentasikan fitur yang belum ada sebagai fitur final.

- [ ] Fase 12: Persiapan adapter PSDK di level desain saja
  - Tujuan: mendokumentasikan rencana adapter PSDK tanpa implementasi DJI.
  - File kemungkinan dibuat/diubah: `DESIGN.md`, mungkin `docs/psdk_migration_notes.md`.
  - Acceptance criteria: boundary `PSDKLiveviewFrameSource` dan `PSDKTelemetryProvider` jelas di level desain.
  - Catatan batasan: jangan menambahkan dependency PSDK atau kode integrasi PSDK asli.
