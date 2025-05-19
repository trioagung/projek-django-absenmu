from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),  # Redirect root ke login
    path("login/", views.custom_login, name="login"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("guru/dashboard/", views.guru_dashboard, name="guru_dashboard"),
    path("siswa/dashboard/", views.siswa_dashboard, name="siswa_dashboard"),
    path('login/', views.custom_login, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tambah-user/', views.tambah_user, name='tambah_user'),
    path('siswa/tambah/', views.tambah_siswa, name='tambah_siswa'),
    path('siswa/', views.daftar_siswa, name='daftar_siswa'),
    path('siswa/<int:siswa_id>/', views.detail_siswa, name='detail_siswa'),
    path('siswa/tambah/', views.tambah_siswa, name='tambah_siswa'),
    path('siswa/edit/<int:siswa_id>/', views.edit_siswa, name='edit_siswa'),
    path('siswa/hapus/<int:siswa_id>/', views.hapus_siswa, name='hapus_siswa'),
    path('absensi/tambah/', views.tambah_absensi, name='tambah_absensi'),
    path('pelanggaran/tambah/', views.tambah_pelanggaran, name='tambah_pelanggaran'),
    path('rekap/kelas/', views.rekap_kelas, name='rekap_kelas'),
    path('rekap/siswa/<int:siswa_id>/', views.rekap_siswa, name='rekap_siswa'),
    path('siswa/keluar/', views.siswa_keluar_list, name='siswa_keluar_list'),
    path('siswa/keluar/<int:siswa_id>/', views.siswa_keluar_action, name='siswa_keluar_action'),


]
