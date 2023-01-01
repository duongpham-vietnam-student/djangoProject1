from django.urls import path
from . import views
from django.urls import path
from . import views
app_name = "schedule"
urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate, name='generate'),
    path('editempl/', views.editempl, name='editempl'),
    path('editcreateemploy/', views.edit_create_employ, name='edit_create'),
    path('editassi/', views.editassi, name='editassi'),
    path('editcreateassi/', views.edit_create_assi, name='edit_create_assi'),
    path('editshift/', views.editshift, name='editshift'),
    path('editcreateshift/', views.edit_create_shift, name='edit_create_shift'),
    path('editunav/', views.editunav, name='editunav'),
    path('editcreateunav/', views.edit_create_unav, name='edit_create_unav')
]