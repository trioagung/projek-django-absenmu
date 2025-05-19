from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Count
import json

from .models import User, Siswa, Kelas, Jurusan, Absensi, Pelanggaran
from .forms import CustomUserCreationForm, UserSiswaForm, SiswaForm, AbsensiForm, PelanggaranForm


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, "Username dan password harus diisi!")
            return render(request, "core/login.html")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "guru":
                return redirect("guru_dashboard")
            elif user.role == "siswa":
                return redirect("siswa_dashboard")
            else:
                messages.error(request, "Role user tidak dikenali!")
                return redirect("login")
        else:
            messages.error(request, "Username atau password salah!")
            return render(request, "core/login.html")
    return render(request, "core/login.html")


@login_required
def admin_dashboard(request):
    return render(request, "core/admin_dashboard.html")


@login_required
def guru_dashboard(request):
    return render(request, "core/guru_dashboard.html")


@login_required
def siswa_dashboard(request):
    return render(request, "core/siswa_dashboard.html")


@login_required
def tambah_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])  # pastikan pakai password1
            user.save()
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/tambah_user.html', {'form': form})


def tambah_siswa(request):
    if request.method == 'POST':
        user_form = UserSiswaForm(request.POST)
        siswa_form = SiswaForm(request.POST)
        if user_form.is_valid() and siswa_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'siswa'
            user.save()

            siswa = siswa_form.save(commit=False)
            siswa.user = user
            siswa.save()

            return redirect('daftar_siswa')
    else:
        user_form = UserSiswaForm()
        siswa_form = SiswaForm()
    return render(request, 'core/tambah_siswa.html', {
        'user_form': user_form,
        'siswa_form': siswa_form,
    })


def daftar_siswa(request):
    siswa_list = Siswa.objects.select_related('user', 'kelas', 'jurusan').all()
    return render(request, 'core/daftar_siswa.html', {'siswa_list': siswa_list})


def detail_siswa(request, siswa_id):
    siswa = get_object_or_404(Siswa, pk=siswa_id)
    return render(request, 'core/detail_siswa.html', {'siswa': siswa})


def tambah_absensi(request):
    jurusan_id = request.GET.get('jurusan')
    kelas_id = request.GET.get('kelas')
    siswa_list = None

    if jurusan_id and kelas_id:
        siswa_list = Siswa.objects.filter(jurusan_id=jurusan_id, kelas_id=kelas_id)

    if request.method == 'POST':
        for key, status in request.POST.items():
            if key.startswith('status_'):
                s_id = key.replace('status_', '')
                if status:
                    Absensi.objects.update_or_create(
                        siswa_id=s_id,
                        tanggal=request.POST['tanggal'],
                        defaults={'status': status}
                    )
        return redirect('tambah_absensi')

    jurusan_list = Jurusan.objects.all()
    kelas_list = Kelas.objects.filter(jurusan_id=jurusan_id) if jurusan_id else []

    context = {
        'jurusan_list': jurusan_list,
        'kelas_list': kelas_list,
        'siswa_list': siswa_list,
    }
    return render(request, 'core/tambah_absensi.html', context)


def tambah_pelanggaran(request):
    jurusan_id = request.GET.get('jurusan')
    kelas_id = request.GET.get('kelas')
    siswa_list = None

    if jurusan_id and kelas_id:
        siswa_list = Siswa.objects.filter(jurusan_id=jurusan_id, kelas_id=kelas_id)

    if request.method == 'POST':
        siswa_id = request.POST.get('siswa')
        tanggal = request.POST.get('tanggal')
        pelanggaran_ids = request.POST.getlist('pelanggaran')

        if siswa_id and tanggal and pelanggaran_ids:
            pelanggaran_obj = Pelanggaran.objects.create(
                siswa_id=siswa_id,
                tanggal=tanggal
            )
            pelanggaran_obj.pelanggaran.set(pelanggaran_ids)
            return redirect('tambah_pelanggaran')

    jurusan_list = Jurusan.objects.all()
    kelas_list = Kelas.objects.filter(jurusan_id=jurusan_id) if jurusan_id else []

    context = {
        'jurusan_list': jurusan_list,
        'kelas_list': kelas_list,
        'siswa_list': siswa_list,
    }
    return render(request, 'core/tambah_pelanggaran.html', context)


def rekap_kelas(request):
    jurusan_id = request.GET.get('jurusan')
    kelas_id = request.GET.get('kelas')
    siswa_list = None
    rekap_data = None
    grafik_data = None

    jurusan_list = Jurusan.objects.all()
    kelas_list = Kelas.objects.filter(jurusan_id=jurusan_id) if jurusan_id else []

    if kelas_id:
        siswa_list = Siswa.objects.filter(kelas_id=kelas_id)

        rekap_data = []
        for siswa in siswa_list:
            absensi = Absensi.objects.filter(siswa=siswa).values('status').annotate(total=Count('status'))
            pelanggaran_count = Pelanggaran.objects.filter(siswa=siswa).count()
            rekap_data.append({
                'siswa': siswa.nama,
                'absensi': {item['status']: item['total'] for item in absensi},
                'pelanggaran_count': pelanggaran_count,
            })

        grafik_data = {
            'labels': [r['siswa'] for r in rekap_data],
            'alfa': [r['absensi'].get('alfa', 0) for r in rekap_data],
            'izin': [r['absensi'].get('izin', 0) for r in rekap_data],
            'bolos': [r['absensi'].get('bolos', 0) for r in rekap_data],
            'pelanggaran': [r['pelanggaran_count'] for r in rekap_data],
        }

    context = {
        'jurusan_list': jurusan_list,
        'kelas_list': kelas_list,
        'siswa_list': siswa_list,
        'rekap_data': rekap_data,
        'grafik_data': json.dumps(grafik_data),
    }
    return render(request, 'core/rekap_kelas.html', context)


def rekap_siswa(request, siswa_id):
    siswa = get_object_or_404(Siswa, pk=siswa_id)

    absensi = Absensi.objects.filter(siswa=siswa).values('status').annotate(total=Count('status'))
    pelanggaran_count = Pelanggaran.objects.filter(siswa=siswa).count()

    rekap_data = {
        'absensi': {item['status']: item['total'] for item in absensi},
        'pelanggaran_count': pelanggaran_count,
    }

    grafik_data = {
        'labels': ['Izin', 'Alfa', 'Bolos', 'Pelanggaran'],
        'data': [
            rekap_data['absensi'].get('izin', 0),
            rekap_data['absensi'].get('alfa', 0),
            rekap_data['absensi'].get('bolos', 0),
            rekap_data['pelanggaran_count'],
        ],
    }

    context = {
        'siswa': siswa,
        'rekap_data': rekap_data,
        'grafik_data': json.dumps(grafik_data),
    }
    return render(request, 'core/rekap_siswa.html', context)


def siswa_keluar_list(request):
    siswa_aktif = Siswa.objects.filter(is_active=True)
    return render(request, 'core/siswa_keluar_list.html', {'siswa_list': siswa_aktif})


def siswa_keluar_action(request, siswa_id):
    siswa = get_object_or_404(Siswa, pk=siswa_id)
    siswa.is_active = False
    siswa.save()
    messages.success(request, f'Siswa {siswa.nama} berhasil ditandai keluar.')
    return redirect('siswa_keluar_list')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Siswa
from .forms import SiswaForm

def edit_siswa(request, siswa_id):
    siswa = get_object_or_404(Siswa, pk=siswa_id)
    if request.method == 'POST':
        form = SiswaForm(request.POST, instance=siswa)
        if form.is_valid():
            form.save()
            return redirect('daftar_siswa')
    else:
        form = SiswaForm(instance=siswa)
    return render(request, 'core/edit_siswa.html', {'form': form})


from django.shortcuts import redirect, get_object_or_404
from .models import Siswa

def hapus_siswa(request, siswa_id):
    siswa = get_object_or_404(Siswa, id=siswa_id)
    siswa.delete()
    return redirect('nama_url_daftar_siswa')  # Ganti dengan URL yang sesuai
