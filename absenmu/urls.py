from django.contrib import admin
from django.urls import path, include

from django.urls import path
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
   # path('login/', include('login.urls')),  # misal untuk login
    path('', include('core.urls')),  # tambahkan ini
    path('login/', views.custom_login, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

]
