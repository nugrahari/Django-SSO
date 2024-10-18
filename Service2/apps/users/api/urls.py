from django.urls import path
from .views import root_view, user_list


urlpatterns = [
    path('', root_view, name='root_view'),
    path('app1/', user_list, name='user-list'),
]
