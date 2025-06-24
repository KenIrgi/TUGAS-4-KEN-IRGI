# Aplikasi Grafis 2D

Aplikasi web interaktif untuk menggambar dan memanipulasi objek grafis 2D dengan berbagai fitur transformasi geometri dan clipping.

## 🎨 Fitur Utama

### Alat Gambar
- **Titik**: Menggambar titik/dot pada canvas
- **Garis**: Menggambar garis lurus
- **Persegi**: Menggambar persegi panjang/kotak
- **Ellipse**: Menggambar ellipse/lingkaran

### Kustomisasi Visual
- **Pemilih Warna**: Color picker untuk mengatur warna objek
- **Ketebalan**: Slider untuk mengatur ketebalan garis (1-10 pixel)
- **Preview Real-time**: Menampilkan preview saat menggambar

### Manajemen Objek
- **Daftar Objek**: Menampilkan semua objek yang telah dibuat
- **Seleksi Objek**: Klik objek di daftar untuk memilih
- **Hapus Objek**: Menghapus objek yang dipilih

### Transformasi Geometri
- **Translasi**: Memindahkan objek dengan nilai dx, dy
- **Rotasi**: Memutar objek dengan sudut dalam derajat
- **Skala**: Mengubah ukuran objek dengan faktor sx, sy

### Windowing & Clipping
- **Mode Windowing**: Membuat area window untuk clipping
- **Visual Feedback**: Objek dalam window ditandai dengan warna merah
- **Clipping**: Memotong objek di luar area window

## 🚀 Cara Menggunakan

### Menggambar Objek
1. Pilih alat gambar dari panel sebelah kiri
2. Atur warna dan ketebalan sesuai keinginan
3. Untuk **Titik**: Klik sekali pada canvas
4. Untuk objek lain: Klik dan drag pada canvas

### Memanipulasi Objek
1. Pilih objek dari daftar objek
2. Masukkan nilai transformasi yang diinginkan
3. Klik tombol transformasi yang sesuai:
   - **Translasi**: Memindahkan objek
   - **Rotasi**: Memutar objek dari titik pusatnya
   - **Skala**: Mengubah ukuran objek

### Windowing & Clipping
1. Klik tombol "Mode Windowing"
2. Drag pada canvas untuk membuat area window
3. Objek dalam window akan berubah warna menjadi merah
4. Klik "Clip Objek Windowing" untuk memotong objek di luar window

## 🛠️ Teknologi yang Digunakan

- **HTML5 Canvas**: Untuk rendering grafis 2D
- **JavaScript**: Logika aplikasi dan manipulasi objek
- **CSS3**: Styling antarmuka pengguna
- **Responsive Design**: Layout yang adaptif

## 📋 Struktur Kode

### Variabel Global
- `objects[]`: Array untuk menyimpan semua objek
- `selectedObject`: Objek yang sedang dipilih
- `currentTool`: Alat gambar yang aktif
- `windowRect`: Area window untuk clipping

### Fungsi Utama
- `createPoint()`: Membuat objek titik
- `createShape()`: Membuat objek garis, persegi, atau ellipse
- `drawObject()`: Merender objek ke canvas
- `applyTransformation()`: Menerapkan transformasi geometri
- `clipObjects()`: Melakukan clipping berdasarkan window

### Event Handling
- Mouse events untuk interaksi drawing
- Form events untuk pengaturan tool dan properties
- Real-time preview saat drawing

## 🎯 Fitur Transformasi Geometri

### Translasi
Memindahkan objek dengan rumus:
```
x' = x + dx
y' = y + dy
```

### Rotasi
Memutar objek terhadap titik pusatnya dengan transformasi matrix 2D.

### Skala
Mengubah ukuran objek dengan faktor pengali:
```
width' = width × sx
height' = height × sy
```

## 📐 Algoritma Clipping

Aplikasi menggunakan algoritma clipping sederhana dengan pemeriksaan bounding box:
1. Menentukan area window
2. Mengecek setiap objek apakah berada dalam window
3. Objek di luar window dihapus (clipped)
4. Objek dalam window dipertahankan

## 🎨 Antarmuka Pengguna

### Panel Kiri (Sidebar)
- **Pilih Alat Gambar**: Radio button untuk memilih tool
- **Warna & Ketebalan**: Color picker dan slider
- **Daftar Objek**: List objek dengan fungsi select dan delete
- **Transformasi**: Input fields dan tombol untuk transformasi
- **Windowing & Clipping**: Kontrol untuk operasi clipping

### Area Canvas
- **Canvas**: Area gambar utama 800x600 pixel
- **Status Bar**: Menampilkan koordinat mouse real-time
- **Visual Feedback**: Preview dengan garis putus-putus

## 🔧 Instalasi dan Penggunaan

1. Simpan kode sebagai file `.html`
2. Buka file dengan web browser modern
3. Tidak memerlukan server web atau dependensi tambahan
4. Kompatibel dengan Chrome, Firefox, Safari, Edge

## 📝 Catatan Teknis

- Canvas berukuran 800x600 pixel
- Transformasi menggunakan Canvas 2D context API
- State management menggunakan JavaScript objects
- Event-driven architecture untuk interaktivitas
- Responsive design dengan flexbox layout

## 🚀 Pengembangan Lanjutan

Fitur yang dapat ditambahkan:
- Save/Load gambar
- Undo/Redo functionality
- Layer management
- Algoritma clipping yang lebih advanced (Cohen-Sutherland, Liang-Barsky)
- Export ke format file (PNG, SVG)
- Zooming dan panning
- Grid dan snap-to-grid
- Shape tools yang lebih banyak (polygon, bezier curve)

## 📄 Lisensi

Aplikasi ini dapat digunakan untuk tujuan edukasi dan pengembangan.