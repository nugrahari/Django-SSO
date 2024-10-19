from django.urls import path, include

urlpatterns = [
    path('api/', include('apps.auths.api.urls')),  # Pastikan ini sesuai dengan nama aplikasi Anda
]
