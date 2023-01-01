from django.urls import path
from . import views
app_name = "user"
urlpatterns = [
    path('/request', views.requ, name ="request"),
    path('/setup', views.setup, name ="setup"),
    path('/setting', views.sett, name ="setting"),
    path('/changeinfo2', views.changeinfouser2, name = "changeinfouser2"),
    path('/changeinfo1', views.changeinfouser1, name = "changeinfouser1"),
    path('/accept', views.accept, name = "accept"),
    path('/navi', views.navi, name="navi"),
]
