from django.urls import path

from user import views

urlpatterns = [
    path('create/', views.UsercreateAPI.as_view(), name='create'),
    path('login/', views.UserLoginAPI.as_view(), name='Login'),
]