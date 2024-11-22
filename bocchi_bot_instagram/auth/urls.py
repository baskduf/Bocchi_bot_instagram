
from . import views
from django.urls import path

urlpatterns = [
    path('data-deletion/', views.data_deletion_request, name='data_deletion'),
    path('login/', views.instagram_login, name='instagram_login'),
    path('callback/', views.instagram_callback, name='instagram_callback'),
    path('delete_status/', views.delete_status, name='delete_status'),
]
