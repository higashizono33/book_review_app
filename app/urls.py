from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:pk>', BookDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', delete_book, name='delete'),
    path('add_favorite/<int:pk>/<str:page>', add_favorite, name='add_favorite'),
    path('remove_favorite/<int:pk>/<str:page>', remove_favorite, name='remove_favorite'),
]