# Dokumentasi Client

Kelas `Client` bertanggung jawab untuk mengirim request gambar dan layanan yang diminta ke broker. Request yang dikirim mencakup layanan yang diinginkan (`operation`) dan gambar yang akan diproses. Setelah broker mengembalikan hasilnya, client menampilkan gambar sebelum dan sesudah diproses.

## Struktur Kelas

### `__init__` Method
```python
    def __init__(self, address, port):
        # Alamat broker
        self.address = address
        # Port broker
        self.port = port
```
- `address`: Alamat server broker
- `port`: Port broker.

### `send_request` Method
```python
    def send_request(self, operation, image_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Menghubungkan ke broker
            client_socket.connect((self.address, self.port))
            # Membuka gambar
            image = Image.open(image_path)
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            # Encode gambar base64
            base64_image = base64.b64encode(buffer.getvalue()).decode()
            
            # Format dictionary
            request = str({'operation': operation, 'data': base64_image})
            # Mengirimkan permintaan ke broker
            client_socket.sendall(request.encode())
            print(f"Gambar {image_path} dengan ukuran {len(buffer.getvalue())} bytes telah dikirim ke broker.")

            # Menerima hasil dari broker
            response_data = client_socket.recv(BUFFER_SIZE).decode()
            # Decode hasil dari broker
            result_image_data = base64.b64decode(response_data + "===")
            # Membuka hasil sebagai gambar
            result_image = Image.open(io.BytesIO(result_image_data))

            # Menampilkan gambar sebelum dan sesudah
            self.display_images(image, result_image)
```
- Membuat koneksi ke server broker menggunakan socket.
- Membuka gambar dari path yang diberikan (`image_path`) dan mengonversinya ke format base64 untuk dikirim.
- Membentuk request dictionary yang berisi `operation` (layanan yang diinginkan) dan `data` (gambar dalam format base64).
- Mengirim request ke broker dan menunggu respons.
- Decode gambar hasil pemrosesan dari broker, membuka gambar tersebut, dan memanggil `display_images` untuk menampilkan gambar sebelum dan sesudah diproses.

### `display_images` Method
```python
    def display_images(self, original_image, result_image):
        # Mengatur figure untuk plotting
        plt.figure(figsize=(12, 6))  # Lebar 12, tinggi 6
        
        # Plot gambar asli
        plt.subplot(1, 2, 1)
        plt.imshow(original_image)
        plt.title('Gambar Asli')
        plt.axis('off')

        # Mengubah gambar ke numpy array
        # untuk cek hasil gambar
        # menggunakan layanan grayscale atau enhance
        result_image_np = np.array(result_image)
    
        # Plot gambar hasil pemrosesan
        plt.subplot(1, 2, 2)
        # Jika grayscale (2D array)
        if len(result_image_np.shape) == 2:
            plt.imshow(result_image, cmap='gray')
        # Jika berwarna (3D array)
        else:
            plt.imshow(result_image)
        plt.title('Gambar Setelah Pemrosesan')
        plt.axis('off')

        # Menampilkan kedua gambar dalam satu window
        plt.show()
```
- Menampilkan gambar asli dan gambar hasil pemrosesan secara berdampingan menggunakan Matplotlib.
- Jika hasil gambar dalam bentuk grayscale (2D array), maka menampilkannya dalam mode grayscale
- Jika berwarna, menampilkannya secara normal.
