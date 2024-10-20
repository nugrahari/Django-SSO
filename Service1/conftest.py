import pytest
from django.contrib.auth.models import User


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture(autouse=True)
def setup_redis_cache(settings):
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # Backup hasher
    ]
    settings.CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://:dev_password@localhost:6379/4',  # Redis URL with password
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
