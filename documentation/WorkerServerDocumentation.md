# Dokumentasi WorkerServer

Kelas `WorkerServer` adalah kelas yang bertanggung jawab untuk menerima permintaan gambar dari broker, dan memproses gambar berdasarkan layanan yang diminta (`Long-Enhance` untuk enhance gambar atau `Short-Grayscale` untuk mengubah gambar ke grayscale).

## Struktur Kelas

### `__init__` Method
```python
    def __init__(self, id, address, port):
        # ID untuk identifikasi worker
        self.id = id
        # Alamat worker
        self.address = address
        # Port worker
        self.port = port
```
- `id`: ID untuk identifikasi worker.
- `address`: Alamat server worker.
- `port`: Port yang digunakan oleh worker.

### `start` Method
```python
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.address, self.port))
            server.listen()
            print(f"Worker {self.id} running di {self.address}:{self.port}")
            while True:
                # Menerima koneksi
                client_socket, client_address = server.accept()
                # Thread baru untuk menangani permintaan
                threading.Thread(target=self.handle_request, args=(client_socket,)).start()
```
- Membuat socket server untuk menerima koneksi dari broker.
- Setiap request yang diterima akan ditangani oleh thread baru dengan memanggil method `handle_request`.

### `handle_request` Method
```python
    def handle_request(self, client_socket):
        with client_socket:
            # Menerima data dari broker
            data = client_socket.recv(BUFFER_SIZE).decode()
            # Mengkonversi string ke dictionary
            request = eval(data)
            # Mengambil layanan (operation) yang dipilih
            operation = request.get('operation')
            # decode base64
            image_data = base64.b64decode(request.get('data') + "===")
            # Membaca gambar
            image = Image.open(io.BytesIO(image_data))
            
            print(f"Worker {self.id} menerima gambar berukuran {image.size}.")

            # Memproses gambar berdasarkan layanan yang di minta
            if 'Long-Enhance' in operation:
                result_image = self.enhance_image(image)  # Meningkatkan gambar
            elif 'Short-Grayscale' in operation:
                result_image = self.convert_to_grayscale(image)  # Mengubah gambar menjadi grayscale

            print(f"Worker {self.id} memproses gambar.")
            
            # Menyimpan hasil gambar ke buffer
            output_buffer = io.BytesIO()
            # Menyimpan hasil sebagai buffer
            result_image.save(output_buffer, format="JPEG")
            # Encode hasil gambar ke base64
            base64_output = base64.b64encode(output_buffer.getvalue()).decode()
            # Mengirim hasil kembali ke broker
            client_socket.sendall(base64_output.encode())
            
            print(f"Worker {self.id} telah mengirim hasil kembali ke broker.")
```
- Menerima data dari broker, yang berupa gambar dalam format base64 beserta jenis operasi atau layanan yang diminta.
- Memproses gambar berdasarkan layanan (`Long-Enhance` untuk peningkatan gambar, `Short-Grayscale` untuk konversi grayscale).
- Mengirimkan kembali gambar yang sudah diproses dalam format base64 ke broker.

### `enhance_image` Method
```python
    def enhance_image(self, img):
        # Meningkatkan kecerahan gambar
        enhancer = ImageEnhance.Brightness(img)
        img_bright = enhancer.enhance(1.15)

        # Meningkatkan kontras
        enhancer_contrast = ImageEnhance.Contrast(img_bright)
        img_contrast = enhancer_contrast.enhance(1.1)

         # Menerapkan median filter untuk mengurangi noise
        img_filtered = img_contrast.filter(ImageFilter.MedianFilter(size=1))
        
        return img_filtered
```
- Meningkatkan kecerahan gambar sebesar 1.15 kali.
- Meningkatkan kontras gambar sebesar 1.1 kali.
- Mengurangi noise dengan menerapkan filter median.
- Mengembalikan gambar yang telah ditingkatkan.

### `convert_to_grayscale` Method
```python
    def convert_to_grayscale(self, img):
        # Mengonversi gambar ke grayscale
        return img.convert('L')
```
- Mengonversi gambar menjadi grayscale dan mengembalikan hasilnya.
