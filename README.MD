# Docker Compose untuk Aplikasi Django dengan Nginx dan Redis

Dokumen ini memberikan panduan tentang cara menjalankan aplikasi Django dengan Nginx dan Redis menggunakan Docker Compose. Aplikasi ini terdiri dari tiga layanan Django (`django_svc1`, `django_svc2`, dan `django_svc3`), dan menggunakan Redis sebagai cache.

## Daftar Isi

- [Prasyarat](#prasyarat)
- [Instalasi dan Persiapan](#instalasi-dan-persiapan)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Menjalankan Unit Test](#menjalankan-unit-test)
- [Konfigurasi Nginx](#konfigurasi-nginx)
- [Koneksi ke Redis](#koneksi-ke-redis)
- [Host dan Port yang Dapat Diakses](#host-dan-port-yang-dapat-diakses)
- [Penjelasan](#penjelasan)

## Prasyarat

Sebelum menjalankan aplikasi, pastikan Anda telah menginstal perangkat lunak berikut:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Py-Poetry](https://python-poetry.org/docs/)

## Instalasi dan Persiapan

1. Clone repositori ini ke mesin lokal Anda:
   ```bash
   git clone https://github.com/nugrahari/Django-SSO.git
   cd Django-SSO
   poetry install
   ```
2. Pastikan semua dependensi Python yang diperlukan telah didefinisikan dalam file requirements.txt di masing-masing direktori Service1, Service2, dan Service3. Contoh requirements.txt untuk Django:
   ```plaintext
   asgiref==3.8.1
   cffi==1.17.1
   cryptography==43.0.1
   Django==5.1.2
   grpcio==1.67.0
   uvicorn==0.32.0
   ...
   ```

## Menjalankan Aplikasi

Untuk menjalankan aplikasi, gunakan perintah berikut di direktori root proyek Anda:

```bash
docker-compose up --build
```

Perintah ini akan membangun dan memulai semua layanan yang terdaftar dalam docker-compose.yml. Setelah semua layanan berjalan, Anda dapat mengakses aplikasi melalui browser atau alat pengujian API.

## Menjalankan Unit Test

Untuk menjalankan auto unit test, dapat dilakukan menggunakan perintah berikut:

```bash
cd Service1
pytest --cov=. --cov-report=html
```

## Konfigurasi Nginx

Nginx digunakan sebagai reverse proxy untuk mengarahkan permintaan ke layanan Django. Pastikan Anda telah mengkonfigurasi file nginx/nginx.conf sesuai kebutuhan. Berikut adalah bagian penting dari konfigurasi Nginx:

```bash
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;


    client_max_body_size 0;
    proxy_request_buffering off;

    server {
        listen 80 ;  # Hanya gunakan listen 80 untuk HTTP
        server_name _;

        location /static/ {
            alias /app/service1/staticfiles/;  # Ganti dengan path ke direktori static Anda
        }

        location / {
            proxy_pass http://django_svc1:8000;  # Arahkan ke service Django
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    server {
        listen 802 http2;
        include config/grpc-header-config.conf;

        location /grpc {
            auth_request_set $auth_status $upstream_http_x_auth_status;
            grpc_pass grpc://django_svc1:50051;
        }
        default_type application/grpc;
    }
}
```

Dengan configurasi diatas, kita bisa mengakses django_service1 langsung tanpa port, dan juga grpc server di http2

## Koneksi ke Redis

Aplikasi ini menggunakan Redis sebagai cache. Pastikan Anda mengkonfigurasi koneksi Redis di pengaturan Django Anda. Contoh pengaturan di settings.py:

```bash
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': 'dev_password',  # Ganti dengan password yang Anda tentukan
        }
    }
}
```

Redis ini digunakan untuk menyimpan token yang di blacklist saat user logout agar tidak dapat digunakan diaplikasi manapun

## Host dan Port yang Dapat Diakses

Setelah menjalankan aplikasi, Anda dapat mengakses layanan-layanan berikut:

- Django Service 1:
  - http server: http://localhost:8000/ atau http://localhost/ (ditangani oleh nginx)
  - GRPC Server: grpc://django_svc1:50051 atau http://localhost:802/grpc/ (ditangani oleh nginx)
- Django Service 2: http://localhost:8001/
- Django Service 3: http://localhost:8002/
- Redis: redis://localhost:6379 dengan password dev_password

## Penjelasan

# Penjelasan Jawaban dari tiap Soal Take Home Test

## 1: Django + gRPC Integration

### - Struktur proyek

Struktur project saya menempatkan semua app kedalam folder apps agar lebih rapih dan menempatkan config deployemnet ke dalam folder settings

### - Mengintegrasikan gRPC dan Django

Grpc server berada di Service1 dan bisa menggunakan command dibawah untuk running server

```
python manage.py run_grpc_server
```

### - Menangani server untuk gRPC dan REST API secara bersamaan

Saya menanganinya menggunakan asynio di file run.py, root_directory Service1

```
cd Service1
python run.py
```

### - Reverse proxy menggunakan Nginx

[Konfigurasi Nginx](#konfigurasi-nginx)

### - Efisiensi dan dokumentasi yang jelas

Saya membuat semua service automatis menggunakan docker compose agar lebih efisien dan semoga readme file ini memudahkan saat running nya

### - Test GRPC Client

Untuk mencoba grpc sebagai client, dapat menggunakan api dari Service2, dengan endpoint ini : /v1/user/api/app1/

## 2: Implementasi Single Sign-On (SSO)

### - Implementasikan sistem SSO untuk ketiga aplikasi Django tersebut

Ke 3 service diatas sudah mendukung SSO, sehingga token yang dihasilkan di Service 1 dapat digunakan untuk request API Service 2

### - Sistem SSO harus mendukung JWT

Sistem login token diatas sudah menggunakan JWT

### - Gunakan secret key dari masing-masing aplikasi Django untuk memverifikasi JWT pada SSO.

Aplikasi ini masih menggunakan secret key JWT Token yang sama

### - Dukungan untuk logout global

Sistem SSO diatas sudah mendukung global logout dengan menggunakan redis untuk menyimpan token yang sudah logout agar ter blacklist sehingga tidak dapat digunakan lagi

### - Penjelasan Singkat

Redis lebih efisien dalam menyimpan data sementara, dan kenapa token yang disimpan adalah yang tidak valid, bukan yang valid, itu dilakukan untuk menhindari penumpukan user login di redis dan mengurangi resiko down

## 3: Custom Password Hashing with Unified Secret Key

### - Implementasi dari CustomPBKDF2PasswordHasher

implementasi dapat di lihat di file berikut

```
~/user1$ cat Service1/apps/auths/libs.py line 34

class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    def encode(self, password, salt, iterations=None):
        secret_key = settings.SECRET_KEY
        # Combine password with secret key for additional security
        combined_password = f"{password}{secret_key}"
        return super().encode(combined_password, salt, iterations)

    def verify(self, password, encoded):
        secret_key = settings.SECRET_KEY
        combined_password = f"{password}{secret_key}"
        return super().verify(combined_password, encoded)
```

CustomPBKDF2PasswordHasher diatas sudah menggunakan dari masing masing secret key django,

### - Fungsi validasi password

contoh fungsi validasi passoword

```
def validate_password(password, encoded_password):
    hasher = CustomPBKDF2PasswordHasher()
    return hasher.verify(password, encoded_password)
```

Fungsi validasi diatas automatis digunakan oleh django, sesuai settings berikut.

```
~/user1$ cat Service1/settings/settings.py line 145

PASSWORD_HASHERS = [
    # Masukkan path ke hasher yang telah dibuat
    'apps.auths.libs.CustomPBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # Backup hasher
]
```

### - Penjelasan tentang keamanan hash password

PBKDF2 (Password-Based Key Derivation Function 2) adalah algoritma hashing yang aman dan telah terbukti efektif dalam melindungi password. Berikut adalah alasan penggunaannya:

Keamanan: PBKDF2 menggunakan salt untuk setiap password yang di-hash, sehingga dua password identik akan menghasilkan hash yang berbeda.
Daya Tahan terhadap Serangan Brute-force: PBKDF2 dapat diatur untuk melakukan banyak iterasi, yang membuat proses hashing lebih lambat dan memperlambat penyerang yang mencoba menebak password.
Standar: PBKDF2 adalah standar yang direkomendasikan oleh NIST dan banyak digunakan di berbagai aplikasi.

### - Alternatif algoritma hashing dan kapan kita perlu menggantinya

Berikut adalah beberapa alternatif algoritma hashing yang umum digunakan untuk mengamankan password, beserta penjelasan singkat dan kapan sebaiknya kita mempertimbangkan untuk menggantinya:

1. Bcrypt,
   Bcrypt adalah algoritma hashing yang dirancang khusus untuk menyimpan password. Ia menggunakan salt dan dapat diatur untuk mengubah tingkat kesulitan hashing (cost factor).
   Kapan Mengganti: Jika aplikasi Anda mulai mengalami serangan brute-force yang efektif atau jika terdapat algoritma hashing yang lebih kuat atau lebih efisien yang muncul, pertimbangkan untuk beralih ke bcrypt atau menyesuaikan cost factor.
2. Scrypt,
   Scrypt adalah algoritma hashing yang lebih baru yang dirancang untuk tahan terhadap serangan berbasis hardware. Ia membutuhkan memori yang signifikan untuk melakukan hashing, sehingga lebih sulit untuk menjalankan serangan brute-force dengan ASIC.
   Kapan Mengganti: Jika Anda memerlukan perlindungan tambahan terhadap serangan berbasis hardware dan kinerja aplikasi Anda memadai untuk menggunakan algoritma yang lebih berat.
3. Argon2,
   Argon2 adalah pemenang Password Hashing Competition dan dirancang untuk keamanan yang lebih baik dengan menggabungkan penggunaan CPU dan memori. Ini juga memungkinkan penyesuaian untuk memori dan waktu hashing.
   Kapan Mengganti: Jika Anda ingin menggunakan algoritma yang paling modern dan aman, atau jika kebijakan keamanan organisasi Anda memperbarui standar hashing password.
   Kapan Perlu Mengganti Algoritma Hashing?
   Anda sebaiknya mempertimbangkan untuk mengganti algoritma hashing password jika:

Algoritma Usang: Algoritma hashing yang Anda gunakan sudah dianggap tidak aman atau sudah terbukti rentan terhadap serangan (misalnya, MD5 dan SHA-1).
Kinerja Terpengaruh: Aplikasi Anda mengalami penurunan performa akibat serangan brute-force, dan algoritma baru dapat memberikan perlindungan lebih baik dengan kinerja yang masih dapat diterima.
Regulasi Keamanan: Kebijakan atau regulasi baru di organisasi Anda memerlukan penggunaan algoritma hashing yang lebih kuat atau terbaru.
Kemunculan Teknik Serangan Baru: Jika ada laporan tentang teknik baru yang mengancam keamanan algoritma hashing yang sedang digunakan.
Mengganti algoritma hashing bukanlah langkah yang sepele; Anda perlu merencanakan dengan hati-hati untuk menghindari masalah seperti kehilangan akses pengguna yang ada. Idealnya, Anda harus memiliki proses migrasi untuk memperbarui password yang di-hash saat pengguna masuk berikutnya.
