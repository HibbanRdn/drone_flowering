# Agent Working Rules

## Bahasa dan Dokumentasi

- Gunakan bahasa Indonesia untuk dokumentasi project.
- Gunakan gaya formal, teknis, dan mudah dipahami.
- Update `README.md` bila cara menjalankan aplikasi berubah.
- Update `TASKS.md` setiap selesai task implementasi.

## Prinsip Implementasi

- Prioritaskan MVP kecil yang dapat diuji.
- Gunakan kode modular dan mudah diuji.
- Jaga boundary antara frame source, inference engine, telemetry provider, result writer, overlay renderer, dan config loader.
- Jelaskan perubahan sebelum dan sesudah implementasi.
- Hindari abstraksi tambahan yang belum dibutuhkan.
- Gunakan target migration PSDK Liveview dan Manifold Application hanya sebagai arah desain sampai ada instruksi eksplisit untuk integrasi.

## Larangan Tahap Saat Ini

- Jangan hardcode path absolut.
- Jangan memakai credential, token, secrets, cloud, S3, atau database production.
- Jangan masuk ke DJI PSDK asli sebelum diminta.
- Jangan membuat Manifold 3 deployment sebelum diminta.
- Jangan membuat DPK packaging sebelum diminta.
- Jangan membuat DJI Pilot rendering sebelum diminta.
- Jangan membuat flight control atau gimbal control.
- Jangan membuat training model serius.
- Jangan membuat fitur production.

## Git dan Naming

- Gunakan nama branch dan commit yang profesional, netral, dan deskriptif bila nanti dibutuhkan.
- Hindari nama branch yang terlalu informal atau terlalu spesifik pada eksperimen sementara.
- Jangan menghapus perubahan user tanpa instruksi eksplisit.

## Validasi

- Untuk perubahan non-trivial, tambahkan pengecekan terkecil yang relevan.
- Pastikan output tetap mengikuti `DATA_SCHEMA.md`.
- Update `DATA_SCHEMA.md` bila field output berubah.
- Pastikan tidak ada credential atau path absolut yang masuk ke repository.

## RTK Usage for Codex

Use RTK for terminal commands that may produce long output, so Codex receives compact and relevant results.

Prefer these commands:
- `rtk git status`
- `rtk git diff`
- `rtk git log`
- `rtk find . -maxdepth 2 -type f`
- `rtk rg "<keyword>" .`
- `rtk ls`
- `rtk cat <file>`

Avoid raw noisy commands when RTK alternatives are available, especially:
- `find`
- `tree`
- `git diff`
- `git log`
- `cat` on long files
- `rg` with broad search scope

Project safety rules:
- Do not commit, push, deploy, install triggers, or change production/backend resources unless explicitly instructed.
- This project is still a planning/offline prototype for Drone Flowering.
- Focus on documentation, PRD, design, data schema, runbook, experiments, and task breakdown.
- Do not add DJI PSDK, Manifold, production S3, or external system integration unless explicitly requested.