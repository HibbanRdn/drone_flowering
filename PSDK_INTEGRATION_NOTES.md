# PSDK Integration Notes

## Ringkasan

Project `drone_plot_gap` adalah offline prototype untuk deteksi plot bolong / missing plant pada kebun nanas. Pipeline saat ini berjalan lokal di laptop dengan input video file, frame sampling, dummy inference, mock telemetry, output `JSONL`/`CSV`, run manifest, run summary, dan overlay lokal.

DJI Payload SDK digunakan sebagai target migrasi desain untuk tahap berikutnya saat DJI Matrice 400 dan DJI Manifold 3 sudah tersedia. Tahap saat ini belum mengimplementasikan PSDK asli, belum membuat Manifold deployment, belum membuat DPK, dan belum menjalankan sample PSDK dari project ini.

DJI Developer App untuk Payload SDK - Manifold 3 sudah dibuat. Nilai App ID, App Key, App License, App Advanced License, dan developer account tidak boleh ditulis di repository, dokumentasi, commit, atau GitHub.

## Lokasi Payload SDK Lokal

Payload SDK resmi tersedia secara lokal di:

```text
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master
```

Folder tersebut adalah SDK resmi DJI dan tidak boleh diubah dari project ini. Gunakan folder tersebut sebagai referensi read-only sampai ada instruksi eksplisit untuk build atau menjalankan sample.

## File App Info Manifold 3

File app info yang relevan untuk Manifold 3:

```text
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/samples/sample_c/platform/linux/manifold3/application/dji_sdk_app_info.h
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/samples/sample_c++/platform/linux/manifold3/application/dji_sdk_app_info.h
```

Field yang biasanya perlu diisi di `dji_sdk_app_info.h`:

- `USER_APP_NAME`
- `USER_APP_ID`
- `USER_APP_KEY`
- `USER_APP_LICENSE`
- `USER_DEVELOPER_ACCOUNT`
- `USER_BAUD_RATE`

`USER_APP_ID` di `dji_sdk_app_info.h` harus konsisten dengan `user_app_id` di `samples/sample_c/platform/linux/manifold3/app_json/app.json`.

## Sample PSDK Relevan

Sample platform Manifold 3:

```text
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/samples/sample_c/platform/linux/manifold3
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/samples/sample_c++/platform/linux/manifold3
```

Sample telemetry / FC subscription:

```text
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/samples/sample_c/module_sample/fc_subscription
```

Sample liveview:

```text
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/samples/sample_c/module_sample/liveview
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/samples/sample_c++/module_sample/liveview
```

Untuk Matrice 400 + Manifold 3, sample resmi harus divalidasi terlebih dahulu sebelum membuat custom app deteksi plot bolong. Sample yang paling relevan untuk pipeline ini adalah FC subscription untuk telemetry dan liveview untuk frame source.

## Tool DPK

Tool DPK yang ditemukan:

```text
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/tools/build_dpk/build_dpk.sh
/Users/muhamadhibbanramadhan/Documents/Payload-SDK-master/tools/build_dpk/README.md
```

DPK packaging dilakukan belakangan setelah binary aplikasi, `app.json`, dan metadata aplikasi stabil. Tahap saat ini belum membuat DPK.

## Credential Security

Data berikut bersifat sensitif:

- App ID
- App Key
- App License
- App Advanced License
- Developer account

Aturan keamanan:

- Jangan menulis credential DJI di README, dokumentasi, source code repository, issue, chat publik, atau commit.
- Jangan commit file `dji_sdk_app_info.h` yang sudah diisi credential.
- Jangan push credential ke GitHub.
- Simpan file berisi credential hanya di device atau dev environment lokal yang terkontrol.
- Sebelum commit/push, selalu cek `git status`, `git diff`, dan pencarian string sensitif.

## SSH Awal Manifold 3

Untuk Matrice 400 + Manifold 3, SSH awal kemungkinan memakai E-Port berikut:

| E-Port | IP |
| --- | --- |
| E1 | `192.168.42.120` |
| E2 | `192.168.42.130` |
| E3 | `192.168.42.140` |

Alamat ini digunakan sebagai catatan kesiapan koneksi awal. Detail username, password, key, atau credential akses tidak boleh ditulis di repository.

## Urutan Kerja Saat Manifold 3 Datang

1. SSH ke Manifold.
2. Cek environment: OS, arsitektur, compiler/toolchain, Python 3, `dpkg`, koneksi payload/drone, dan versi firmware.
3. Transfer Payload-SDK ke device atau dev environment yang sesuai.
4. Isi `dji_sdk_app_info.h` secara lokal di device/dev environment.
5. Samakan `USER_APP_ID` dengan `user_app_id` di `app_json/app.json`.
6. Jalankan sample PSDK resmi paling kecil.
7. Uji FC subscription / telemetry.
8. Uji liveview.
9. Baru mulai mapping ke app deteksi plot bolong.
10. DPK dilakukan belakangan setelah binary dan metadata stabil.

## Mapping Prototype Ke PSDK

| Prototype `drone_plot_gap` | Target PSDK |
| --- | --- |
| `VideoFileFrameSource` | PSDK Liveview frame source |
| `MockTelemetryProvider` | PSDK FC subscription / data subscription |
| `DummyInferenceEngine` | Model inference missing plant / plot gap |
| Local overlay | Debug overlay lokal atau optional DJI Pilot / Open AR rendering |
| `JSONL` / `CSV` output | Local output / log di Manifold |

## Batasan Tahap Saat Ini

- Belum ada integrasi DJI PSDK asli.
- Belum ada deployment ke Manifold 3.
- Belum ada DPK packaging.
- Belum ada DJI Pilot rendering.
- Belum ada flight control.
- Belum ada gimbal control.
- Belum ada training model.
- Belum ada cloud, S3, database, atau credential di repository.
