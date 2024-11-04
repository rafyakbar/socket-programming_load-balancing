# Dokumentasi BrokerServer

Kelas `BrokerServer` bertanggung jawab untuk menerima permintaan dari client, memilih worker dengan load atau bobot terendah, dan kemudian meneruskan request ke worker yang dipilih.

## Struktur Kelas

### `__init__` Method
```python
    def __init__(self, address, port):
        # Alamat broker
        self.address = address
        # Port broker
        self.port = port
        # Daftar worker dan inisialisasi bobot
        self.workers = [
            {'id': 1, 'host': 'localhost', 'port': 8001, 'load': 0},
            {'id': 2, 'host': 'localhost', 'port': 8002, 'load': 0},
            {'id': 3, 'host': 'localhost', 'port': 8003, 'load': 0}
        ]
```
- `address`: Alamat server broker.
- `port`: Port yang digunakan oleh broker.
- `workers`: Daftar worker yang tersedia, masing-masing memiliki id, alamat host, port, dan atribut `load` untuk menyimpan beban.

### `start` Method
```python
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.address, self.port))
            server.listen()
            print(f"Broker mendengarkan di {self.address}:{self.port}")
            print("")
            while True:
                # Menerima koneksi dari client
                client_socket, client_address = server.accept()
                # Thread baru untuk menangani permintaan dari client
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
```
- Membuat socket server broker untuk menerima koneksi dari client.
- Setiap request yang diterima akan ditangani oleh thread baru dengan memanggil method `handle_client`.

### `worker_loads` Method
```python
    def worker_loads(self):
        return {f"Worker {w['id']}": w['load'] for w in self.workers}
```
Mengembalikan dictionary yang menunjukkan beban (load) dari masing-masing worker.

### `handle_client` Method
```python
    def handle_client(self, client_socket):
        with client_socket:
            # Menerima data dari client
            data = client_socket.recv(BUFFER_SIZE).decode()
            # Mengkonversi string ke dictionary
            request = eval(data)
            # Mengambil operasi yang diminta
            operation = request.get('operation')
            # Decode data dari client
            image_data = base64.b64decode(request.get('data') + "===")
            # Membuka gambar
            image = Image.open(io.BytesIO(image_data))
            print(f"Broker menerima gambar berukuran {image.size}.")
            print(f"Load worker sebelum: {self.worker_loads()}")
            
            # Memilih worker berdasarkan bobot terendah
            selected_worker = self.select_worker(image, operation)
            print(f"Broker mengirim gambar ke Worker {selected_worker['id']}")
            print(f"Load worker sesudah: {self.worker_loads()}")
            
            response = self.forward_request(selected_worker, data)  # Meneruskan permintaan ke worker
            client_socket.sendall(response.encode())  # Mengirimkan respons ke client
        print("")
```
- Menerima data dari client, yang berupa gambar dalam format base64 dan operasi atau layanan yang diminta.
- Print ukuran gambar yang diterima serta beban masing-masing worker sebelum pemilihan worker.
- Memilih worker yang akan menangani request dengan memanggil metode `select_worker`.
- Meneruskan request ke worker terpilih dan mengirim respons kembali ke client.

### `select_worker` Method
```python
    def select_worker(self, image, operation):
        # Mengambil lebar dan tinggi dari gambar
        width, height = image.size
        # Menghitung bobot gambar (width * height / 100)
        image_weight = int(width * height / 100)
        # Jika layanannya ada enhance gambar, maka dikalikan dengan
        # karena melakukan 3 operasi untuk enhance gambar
        if 'Long-Enhance' in operation:
            image_weight *= 3
        
        # Memilih worker dengan beban terendah
        selected = min(self.workers, key=lambda w: w['load'])
        # Menambahkan atau update bobot pada worker yang terpilih
        selected['load'] += image_weight
        
        return selected
```
- Menghitung bobot gambar berdasarkan lebar dan tinggi beserta layanan yang diminta.
- Jika operasi adalah `Long-Enhance`, bobot gambar dikalikan tiga karena proses ini lebih berat.
- Memilih worker dengan beban terendah untuk menangani request dan memperbarui beban pada worker tersebut.

### `forward_request` Method
```python
    def forward_request(self, worker, request):
        # Mengambil host dan port dari worker
        host, port = (worker['host'], worker['port'])
        # Menghubungkan ke worker dan mengirimkan request
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker_socket:
            # Menghubungkan ke worker
            worker_socket.connect((host, port))
            # Mengirim request ke worker
            worker_socket.sendall(request.encode())
            # Menerima respons dari worker
            response = worker_socket.recv(BUFFER_SIZE).decode()
            
            return response
```
- Menghubungkan ke worker yang dipilih dan mengirimkan permintaan dari client.
- Menerima respons dari worker dan mengembalikan respons tersebut untuk diteruskan ke client.

