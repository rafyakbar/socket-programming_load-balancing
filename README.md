
# Deskripsi Repositori

Repositori ini dibuat untuk memenuhi tugas mata kuliah **Komputasi Jaringan**. Tujuan dari project ini adalah mengimplementasikan sistem load balancing untuk pemrosesan gambar menggunakan arsitektur client-broker-worker.

<img src="/images/diagram-light.png">

Sistem ini bertujuan untuk menyeimbangkan beban pemrosesan gambar di antara beberapa worker agar setiap worker memiliki beban yang optimal.

## Struktur Repositori

1. **Direktori codes**: Berisi kode utama untuk implementasi client, broker, dan worker.
2. **Direktori documentation**: Berisi file-file dokumentasi berbentuk markdown yang menjelaskan detail setiap komponen.
3. **Informasi anggota**: Berisi informasi tentang mahasiswa yang menegerjakan tugas ini.

## Direktori codes

- **classes.py**: File ini memuat class untuk `WorkerServer`, `BrokerServer`, dan `Client`, yang merupakan inti dari sistem ini.
  - `WorkerServer` menangani pemrosesan gambar.
  - `BrokerServer` bertanggung jawab untuk mendistribusikan beban ke worker.
  - `Client` mengirim request ke broker.
- **01 worker-1.ipynb**: Notebook simulasi untuk worker pertama. Worker ini menerima permintaan dari broker dan memproses gambar yang dikirimkan.
- **01 worker-2.ipynb**: Notebook simulasi untuk worker kedua. Fungsinya sama dengan worker pertama, namun beroperasi pada alamat dan port yang berbeda untuk menguji load balancing.
- **01 worker-3.ipynb**: Notebook simulasi untuk worker ketiga. Sama seperti worker lainnya, beroperasi untuk menerima dan memproses gambar dari broker.
- **02 broker.ipynb**: Notebook untuk simulasi broker. Broker menerima permintaan dari client, menyeimbangkan beban di antara worker, dan mengirim request ke worker yang memiliki beban terendah.
- **03 client.ipynb**: Notebook simulasi untuk client. Client mengirimkan request pemrosesan gambar ke broker dengan memilih layanan secara acak (grayscale atau enhancement).

## Direktori documentation

- **Readme.md**: Berisi daftar isi untuk dokumentasi, yaitu `WorkerServer`, `BrokerServer`, dan `Client`.
- **BrokerServerDocumentation.md**: Berisi penjelasan detail mengenai kelas `BrokerServer`, termasuk fungsionalitas load balancing dan cara menangani permintaan dari client.
- **ClientDocumentation.md**: Berisi penjelasan tentang kelas `Client`, yang mengirimkan request gambar dan menampilkan hasil pemrosesan.
- **WorkerServerDocumentation.md**: Berisi dokumentasi tentang kelas `WorkerServer`, yang bertanggung jawab untuk pemrosesan gambar berdasarkan layanan yang diminta oleh broker.

## Informasi Anggota

Project ini dikerjakan oleh:
- Nama: Rafy Aulia Akbar
- NIM: 24051905007
