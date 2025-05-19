from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings  # jika pakai custom User


# ================================
# Custom User Model
# ================================
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('guru', 'Guru'),
        ('siswa', 'Siswa'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


# ================================
# Kelas dan Jurusan
# ================================
class Kelas(models.Model):
    nama = models.CharField(max_length=50)

    def __str__(self):
        return self.nama


class Jurusan(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


# ================================
# Siswa
# ================================
class Siswa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    nis = models.CharField(max_length=20)
    nisn = models.CharField(max_length=20)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)  # atau gunakan ForeignKey ke Kelas jika ingin
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)  # atau ForeignKey ke Jurusan
    alamat = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama


# ================================
# Absensi
# ================================
class Absensi(models.Model):
    STATUS_ABSEN = (
        ('izin', 'Izin'),
        ('alfa', 'Alfa'),
        ('bolos', 'Bolos'),
    )
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_ABSEN)

    def __str__(self):
        return f"{self.siswa.nama} - {self.tanggal} - {self.status}"


# ================================
# Pelanggaran
# ================================
class MasterPelanggaran(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class Pelanggaran(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)
    pelanggaran = models.ManyToManyField(MasterPelanggaran)

    def __str__(self):
        return f"{self.siswa.nama} - {self.tanggal}"
