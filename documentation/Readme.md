
# Dokumentasi Socket Programming - Load Balancing untuk Pemrosesan Gambar

Repositori ini mengimplementasikan sistem load balancing untuk pemrosesan gambar, yang terdiri dari tiga komponen utama: Worker, Broker, dan Client. Setiap komponen memiliki peran dan fungsi tertentu yang berkontribusi dalam mengelola dan memproses permintaan gambar secara efisien.

## Daftar Isi

1. [WorkerServer](WorkerServerDocumentation.md)
   - Dokumentasi `WorkerServer`, bertanggung jawab untuk memproses request gambar dari broker. Worker ini mendukung layanan peningkatan gambar (kecerahan, kontras, pengurangan noise) dan konversi gambar ke grayscale.

2. [BrokerServer](BrokerServerDocumentation.md)
   - Dokumentasi `BrokerServer`, sebagai perantara antara client dan worker. Broker menggunakan mekanisme load balancing untuk memilih worker dengan beban terendah.

3. [Client](ClientDocumentation.md)
   - Dokumentasi `Client`, yang mengirimkan request pemrosesan gambar ke broker dan menampilkan hasilnya. Client ini juga memvisualisasikan gambar sebelum dan sesudah pemrosesan.

---

Untuk memahami fungsionalitas dan cara kerja setiap komponen, silakan lihat dokumentasi lengkapnya melalui tautan di atas.
