from django.urls import path
from api import views

urlpatterns = [
    path('', views.home, name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('tags/<int:pk>', views.tags),
    path("banner/", views.banner),
]
