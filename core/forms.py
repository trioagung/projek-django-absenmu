from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from .models import User, Siswa, Absensi, Pelanggaran, MasterPelanggaran

# ================================
# Form untuk User (Custom)
# ================================
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']


# ================================
# Form untuk User Siswa (menggunakan built-in UserCreationForm)
# ================================
class UserSiswaForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# ================================
# Form untuk Siswa
# ================================
class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = ['nama', 'nis', 'nisn', 'kelas', 'jurusan', 'alamat']


# ================================
# Form untuk Absensi
# ================================
class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ['siswa', 'tanggal', 'status']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
        }


# ================================
# Form untuk Pelanggaran
# ================================
class PelanggaranForm(forms.ModelForm):
    pelanggaran = forms.ModelMultipleChoiceField(
        queryset=MasterPelanggaran.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Pelanggaran
        fields = ['siswa', 'tanggal', 'pelanggaran']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
        }
