# Flowering Data Experiments

## Tujuan Eksperimen Sudut Kamera

Eksperimen data bertujuan menentukan sudut kamera, altitude, speed, dan kondisi pencahayaan yang paling memungkinkan flowering candidate terlihat jelas pada kebun nanas. Hasil eksperimen dipakai untuk memperbaiki strategi pengambilan data, bukan untuk mengklaim akurasi model final.

## Parameter Yang Perlu Dicatat

| Parameter | Deskripsi |
| --- | --- |
| `altitude` | Ketinggian drone dari permukaan referensi. |
| `gimbal_pitch` | Sudut pitch gimbal, misalnya -90, -60, -45, atau -30 derajat. |
| `heading` | Arah hadap drone. |
| `speed` | Kecepatan drone saat merekam. |
| `time_of_day` | Waktu pengambilan data. |
| `lighting` | Kondisi cahaya, misalnya cerah, mendung, backlight, atau low light. |
| `flight_pattern` | Pola terbang, misalnya grid, garis lurus, atau orbit terbatas. |
| `camera_mode` | Mode kamera, resolusi, FPS, dan exposure bila tersedia. |
| `notes_visibility_flowering` | Catatan apakah flowering terlihat jelas atau tidak. |

## Contoh Tabel Skenario

| Skenario | Gimbal Pitch | Altitude | Speed | Tujuan |
| --- | --- | --- | --- | --- |
| Top-down | -90 derajat | Rendah / sedang | Pelan | Melihat pola lahan dan kemungkinan objek dari atas. |
| Oblique 60 | -60 derajat | Rendah / sedang | Pelan | Menilai visibilitas samping tanaman dan flowering. |
| Oblique 45 | -45 derajat | Rendah / sedang | Pelan / sedang | Mencari kompromi antara cakupan dan detail visual. |
| Oblique 30 | -30 derajat | Rendah / sedang | Pelan | Menguji risiko occlusion dan perspektif terlalu miring. |
| Variasi altitude | Sudut tetap | Berubah | Tetap | Menilai batas detail visual terhadap ketinggian. |
| Variasi speed | Sudut tetap | Tetap | Berubah | Menilai blur dan stabilitas frame. |

## Kriteria Evaluasi

- Flowering terlihat atau tidak.
- Tingkat blur.
- Occlusion oleh daun, baris tanaman, atau sudut pandang.
- Annotation confidence dari reviewer manusia.
- Frame stability.
- Risiko false positive.
- Konsistensi tampilan antar frame.
- Kesesuaian sudut kamera dengan kebutuhan inference.

## Catatan Eksperimen

- Catat kondisi lapangan seobjektif mungkin.
- Jangan mencampur kesimpulan kualitas data dengan akurasi model.
- Simpan video dan output run dengan identitas eksperimen yang jelas.
- GPS drone belum otomatis menunjukkan koordinat objek flowering di tanah.
