from django.urls import path
from . import views
app_name = "login"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name ="login"),
    path('index/', views.index, name='index'),
]
#moi app cu tao duong dan cua rieng no, vi da khai bao o main nen no ok het