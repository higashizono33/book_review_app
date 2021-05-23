from django.urls import path
from .views import IndexView, login_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', login_view, name='login_view'),
]