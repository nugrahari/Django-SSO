# Docker Compose untuk Aplikasi Django dengan Nginx dan Redis

Dokumen ini memberikan panduan tentang cara menjalankan aplikasi Django dengan Nginx dan Redis menggunakan Docker Compose. Aplikasi ini terdiri dari tiga layanan Django (`django_svc1`, `django_svc2`, dan `django_svc3`), dan menggunakan Redis sebagai cache.

## Daftar Isi

- [Prasyarat](#prasyarat)
- [Instalasi dan Persiapan](#instalasi-dan-persiapan)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Konfigurasi Nginx](#konfigurasi-nginx)
- [Koneksi ke Redis](#koneksi-ke-redis)
- [Host dan Port yang Dapat Diakses](#host-dan-port-yang-dapat-diakses)

## Prasyarat

Sebelum menjalankan aplikasi, pastikan Anda telah menginstal perangkat lunak berikut:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalasi dan Persiapan

1. Clone repositori ini ke mesin lokal Anda:
   ```bash
   git clone https://github.com/nugrahari/Django-SSO.git
   cd Django-SSO
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
