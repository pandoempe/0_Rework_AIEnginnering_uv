Dataset yang berisi informasi spesifikasi mobil.
Ukuran awal dataset:
- Baris: 205
- Kolom: 30

Mencari data format string
Mencaritahu apakah data berbentuk kategorikal nominal atau ordinal.

Data type string, melakukan cleansing data:
    - menghilangkan spasi di belakang.
    - membuat seluruh huruf menjadi huruf kecil saja.
    - mengisi value yang kosong dengan mencari value yang terseding (Modus).

Untuk data type angka, mengisi value kosong dengan angka rata-rata.

Melakukan drop duplicate row.

TRANSFORMATION.
Kolom Angka, melakukan normalisasi menggunakan Min Max Scaler.
Kolom Teks, melakukan encoding data (merubah teks menjadi angka agar dapat di baca oleh model.) menggunakan fit transform dan frequency encoding (untuk data yang jenisnya banyak).

