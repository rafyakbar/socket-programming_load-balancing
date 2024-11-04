import socket
import threading
import base64
from PIL import Image, ImageEnhance, ImageFilter
import io
import matplotlib.pyplot as plt
import numpy as np

BUFFER_SIZE = 4096 * 15

class WorkerServer:
    def __init__(self, id, address, port):
        # ID untuk identifikasi worker
        self.id = id
        # Alamat worker
        self.address = address
        # Port worker
        self.port = port

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

    def convert_to_grayscale(self, img):
        # Mengonversi gambar ke grayscale
        return img.convert('L')

class BrokerServer:
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

    def worker_loads(self):
        return {f"Worker {w['id']}": w['load'] for w in self.workers}

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

class Client:
    def __init__(self, address, port):
        # Alamat broker
        self.address = address
        # Port broker
        self.port = port

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