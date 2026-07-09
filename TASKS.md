# Implementation Tasks

## Checklist Fase

- [x] Fase 0: Setup repository dan dependency minimal
  - Tujuan: menyiapkan struktur dasar repository dan dependency paling kecil untuk offline prototype.
  - File kemungkinan dibuat/diubah: `pyproject.toml`, `README.md`, `.gitignore`.
  - Acceptance criteria: environment lokal dapat dibuat, dependency inti tercatat, tidak ada dependency DJI atau cloud.
  - Catatan batasan: jangan membuat integrasi PSDK, DPK, credential, atau fitur production.

- [x] Fase 1: Config loader
  - Tujuan: membaca config lokal untuk input video, output folder, sampling, dan mock telemetry.
  - File kemungkinan dibuat/diubah: `configs/offline.json`, `src/drone_plot_gap/config.py`.
  - Acceptance criteria: config valid dapat dibaca; field wajib yang hilang menghasilkan error jelas.
  - Catatan batasan: jangan hardcode path absolut.

- [x] Fase 2: Video reader / frame source
  - Tujuan: membuat `VideoFileFrameSource` untuk membaca frame dari file video lokal.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/frame_source.py`.
  - Acceptance criteria: frame dan metadata dasar dapat dihasilkan dari video.
  - Catatan batasan: belum membuat PSDK Liveview frame source.

- [x] Fase 3: Frame sampling
  - Tujuan: memilih frame berdasarkan interval frame atau interval waktu.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/frame_source.py`, `src/drone_plot_gap/app.py`.
  - Acceptance criteria: jumlah frame yang diproses sesuai config sampling.
  - Catatan batasan: cukup satu strategi sampling sederhana untuk MVP.

- [x] Fase 4: Dummy inference
  - Tujuan: membuat `DummyInferenceEngine` untuk menghasilkan detection terstruktur.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/inference.py`.
  - Acceptance criteria: output detection mengikuti `DATA_SCHEMA.md`.
  - Catatan batasan: jangan training model serius.

- [x] Fase 5: Mock telemetry
  - Tujuan: membuat `MockTelemetryProvider` untuk menyediakan telemetry per frame.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/telemetry.py`.
  - Acceptance criteria: setiap detection memiliki telemetry wajib.
  - Catatan batasan: jangan mengklaim GPS drone sebagai koordinat objek di tanah.

- [x] Fase 6: Result writer JSONL / CSV
  - Tujuan: membuat `JsonlCsvResultWriter`.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/writer.py`, `src/drone_plot_gap/schema.py`.
  - Acceptance criteria: `detections.jsonl` dan `detections.csv` valid dan mengikuti schema.
  - Catatan batasan: writer harus gagal jelas bila output tidak dapat ditulis.

- [x] Fase 7: Output folder per run
  - Tujuan: memastikan setiap eksekusi memiliki folder output sendiri.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/app.py`, `src/drone_plot_gap/writer.py`.
  - Acceptance criteria: output tersimpan di `data/outputs/runs/<run_id>/` tanpa menimpa run lain.
  - Catatan batasan: jangan menghapus output lama secara otomatis.

- [x] Fase 8: Overlay image / video
  - Tujuan: membuat `OpenCvOverlayRenderer` opsional untuk validasi visual.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/overlay.py`.
  - Acceptance criteria: overlay dapat dibuat bila opsi aktif; pipeline data tetap berjalan bila overlay nonaktif.
  - Catatan batasan: overlay bukan pengganti output `JSONL` atau `CSV`.

- [x] Fase 9: CLI sederhana
  - Tujuan: menyediakan perintah menjalankan pipeline dengan config.
  - File kemungkinan dibuat/diubah: `src/drone_plot_gap/app.py`, `src/drone_plot_gap/__main__.py`.
  - Acceptance criteria: app dapat dijalankan dengan `.venv/bin/python -m drone_plot_gap --config configs/offline.json`.
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

- [x] Fase 12: Run manifest, experiment metadata, dan summary report
  - Tujuan: mencatat metadata eksperimen dan ringkasan run untuk audit data top-view/nadir.
  - File kemungkinan dibuat/diubah: `configs/offline.json`, `src/drone_plot_gap/app.py`, `src/drone_plot_gap/config.py`, `src/drone_plot_gap/writer.py`.
  - Acceptance criteria: setiap run menghasilkan `run_manifest.json` dan `run_summary.json`.
  - Catatan batasan: metadata masih offline/manual, bukan telemetry DJI asli.

- [ ] Fase 13: Request dataset asli dari pembimbing/tim
  - Tujuan: mendapatkan contoh data lapangan GGP/GGF untuk case plot bolong / missing plant sebelum menentukan format input, preprocessing, anotasi, dan arah model.
  - File kemungkinan dibuat/diubah: `EXPERIMENTS.md`, `RUNBOOK.md`, catatan lokal non-repository bila data bersifat internal.
  - Acceptance criteria: tersedia 1-3 file contoh top-view/nadir atau orthomosaic dan informasi metadata minimal untuk evaluasi awal.
  - Catatan batasan: jangan memakai dataset publik, auto-download, Roboflow/Kaggle/Mendeley, cloud/S3, API key, training, atau model AI asli.

- [ ] Fase 14: Evaluasi format data asli
  - Tujuan: menentukan apakah pipeline perlu mendukung video top-view, image folder/foto drone, `.tif`/GeoTIFF tiling, atau format lain.
  - File kemungkinan dibuat/diubah: `DESIGN.md`, `RUNBOOK.md`, mungkin task implementasi baru setelah data diterima.
  - Acceptance criteria: keputusan input utama dan kebutuhan preprocessing/anotasi terdokumentasi.
  - Catatan batasan: jangan membuat fitur parser/preprocessing sebelum contoh data diterima.

- [ ] Fase 15: Evaluasi pendekatan model
  - Tujuan: menentukan pendekatan awal setelah dataset asli tersedia, misalnya deteksi tanaman, deteksi plot kosong, segmentation, atau analisis pola barisan.
  - File kemungkinan dibuat/diubah: `DESIGN.md`, `EXPERIMENTS.md`, mungkin task implementasi baru setelah data diterima.
  - Acceptance criteria: pilihan pendekatan model dan kebutuhan anotasi terdokumentasi.
  - Catatan batasan: jangan training model serius atau menambahkan dependency berat sebelum ada keputusan data.

- [ ] Fase 16: Persiapan adapter PSDK di level desain saja
  - Tujuan: mendokumentasikan rencana adapter PSDK untuk DJI Matrice 400 dan DJI Manifold 3 tanpa implementasi DJI.
  - File kemungkinan dibuat/diubah: `DESIGN.md`, `PSDK_INTEGRATION_NOTES.md`.
  - Acceptance criteria: boundary `PSDKLiveviewFrameSource` dan `PSDKTelemetryProvider` jelas di level desain.
  - Catatan batasan: jangan menambahkan dependency PSDK, Manifold deployment, DPK, flight control, gimbal control, atau kode integrasi PSDK asli.

- [x] Fase 17: PSDK documentation sync
  - Tujuan: menyinkronkan dokumentasi project dengan hasil inspeksi read-only DJI Payload-SDK lokal.
  - File kemungkinan dibuat/diubah: `PSDK_INTEGRATION_NOTES.md`, `README.md`, `DEV_STATUS.md`, `TASKS.md`.
  - Acceptance criteria: lokasi SDK, sample Manifold 3, app info, tool DPK, credential security, dan mapping prototype ke PSDK terdokumentasi tanpa credential.
  - Catatan batasan: jangan mengubah folder Payload-SDK, jangan build/run sample, jangan membuat integrasi PSDK asli.

- [ ] Fase 18: Manifold SSH readiness
  - Tujuan: menyiapkan checklist koneksi awal Manifold 3 untuk DJI Matrice 400.
  - File kemungkinan dibuat/diubah: `PSDK_INTEGRATION_NOTES.md`, `RUNBOOK.md`.
  - Acceptance criteria: catatan E-Port, environment check, dan batasan credential terdokumentasi.
  - Catatan batasan: jangan menyimpan username, password, key, App ID, App Key, License, atau credential lain di repository.

- [ ] Fase 19: PSDK sample run
  - Tujuan: menjalankan sample PSDK resmi paling kecil saat Manifold 3 tersedia.
  - File kemungkinan dibuat/diubah: catatan lokal non-repository atau dokumentasi hasil validasi setelah ada izin.
  - Acceptance criteria: sample resmi berjalan dengan App Info lokal di device/dev environment.
  - Catatan batasan: jangan menjalankan sample sebelum Manifold/device siap dan jangan commit file credential.

- [ ] Fase 20: FC subscription validation
  - Tujuan: memvalidasi telemetry/data subscription PSDK untuk kebutuhan metadata pipeline.
  - File kemungkinan dibuat/diubah: catatan validasi, `DESIGN.md`, mungkin adapter design setelah sample resmi sukses.
  - Acceptance criteria: topik telemetry minimum untuk altitude, heading, gimbal pitch, speed, timestamp, dan GPS/RTK dipahami.
  - Catatan batasan: jangan menganggap GPS drone sebagai koordinat objek di tanah.

- [ ] Fase 21: Liveview validation
  - Tujuan: memvalidasi liveview PSDK sebagai calon frame source top-view/nadir.
  - File kemungkinan dibuat/diubah: catatan validasi, `DESIGN.md`, mungkin adapter design setelah sample resmi sukses.
  - Acceptance criteria: stream liveview dapat dipahami sebagai input frame source dan keterbatasan Matrice 400 + Manifold 3 terdokumentasi.
  - Catatan batasan: jangan menambahkan decoder/model/dependency berat sebelum kebutuhan data jelas.

- [ ] Fase 22: Plot gap adapter design
  - Tujuan: mendesain mapping dari `VideoFileFrameSource`, `MockTelemetryProvider`, dan `DummyInferenceEngine` ke adapter PSDK.
  - File kemungkinan dibuat/diubah: `DESIGN.md`, `PSDK_INTEGRATION_NOTES.md`.
  - Acceptance criteria: desain adapter jelas di level interface tanpa implementasi DJI asli.
  - Catatan batasan: jangan membuat flight control, gimbal control, atau integrasi production.

- [ ] Fase 23: DPK packaging later
  - Tujuan: menyiapkan rencana packaging DPK setelah binary dan metadata aplikasi stabil.
  - File kemungkinan dibuat/diubah: `PSDK_INTEGRATION_NOTES.md`, `RUNBOOK.md`.
  - Acceptance criteria: tool `tools/build_dpk/build_dpk.sh` dan kebutuhan `app_json/app.json` dipahami.
  - Catatan batasan: jangan membuat DPK pada tahap dokumentasi ini.

## Catatan Task Selesai

- [x] 2026-07-03: Menambahkan dokumentasi status development dan panduan demo/manual check.
  - File dibuat/diubah: `DEV_STATUS.md`, `README.md`, `TASKS.md`.
  - Acceptance criteria: status fitur selesai, batasan scope, command manual check, panduan demo, checklist pembimbing, pertanyaan lanjutan, dan paragraf status singkat terdokumentasi.
  - Catatan batasan: tidak menambahkan fitur baru, dependency, schema output, integrasi DJI/PSDK/Manifold, cloud, atau model AI asli.

- [x] 2026-07-09: Menyesuaikan konteks project dari flowering ke plot bolong / missing plant.
  - File dibuat/diubah: `README.md`, `PRD.md`, `DESIGN.md`, `DATA_SCHEMA.md`, `TASKS.md`, `EXPERIMENTS.md`, `RUNBOOK.md`, `DEV_STATUS.md`, `configs/offline.json`, `tests/test_pipeline_smoke.py`, `src/drone_plot_gap/__main__.py`, `pyproject.toml`.
  - Acceptance criteria: dokumentasi, metadata default, label dummy, dan smoke test memakai `target_case` `missing_plant`, `camera_view` `nadir`, dan label `empty_plot_candidate`.
  - Catatan batasan: tidak rename folder project, tidak mengubah kontrak record detection, tidak menambahkan fitur baru, dependency, DJI PSDK, deployment Manifold, DPK, flight/gimbal control, cloud/S3, credential, training, atau model AI asli.

- [x] 2026-07-09: Rename/rebranding package project menjadi `drone_plot_gap`.
  - File/folder dibuat/diubah: `src/drone_plot_gap/`, `pyproject.toml`, `tests/test_pipeline_smoke.py`, `README.md`, `PRD.md`, `DESIGN.md`, `DATA_SCHEMA.md`, `TASKS.md`, `EXPERIMENTS.md`, `RUNBOOK.md`, `DEV_STATUS.md`.
  - Acceptance criteria: package Python, command module, import test, entrypoint project, dokumentasi, dan `schema_version` memakai nama baru `drone_plot_gap` / `drone-plot-gap-detection.v1`.
  - Catatan batasan: hanya rename/rebranding; tidak menambah fitur, dependency, integrasi DJI PSDK, deployment Manifold, DPK, DJI Pilot rendering, flight/gimbal control, training model, cloud/S3, database, atau credential.

- [x] 2026-07-09: Menambahkan dokumentasi integrasi PSDK sebagai target migrasi.
  - File dibuat/diubah: `PSDK_INTEGRATION_NOTES.md`, `README.md`, `DEV_STATUS.md`, `TASKS.md`.
  - Acceptance criteria: hubungan prototype offline dengan Payload-SDK, lokasi SDK lokal, file app info Manifold 3, sample relevan, tool DPK, credential security, urutan kerja Manifold 3, dan mapping prototype ke PSDK terdokumentasi.
  - Catatan batasan: tidak mengubah Payload-SDK, tidak memasukkan credential, tidak build/run sample, tidak membuat DPK, tidak menambah dependency, dan tidak membuat integrasi DJI asli.
