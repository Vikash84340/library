from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, date

from .models import Student, Attendance, Payment
from .forms import StudentForm

import qrcode
import base64
from io import BytesIO


# ---------------- HOME ----------------
def home(request):
    return render(request, 'home.html')


# ---------------- LOGIN ----------------
def student_login(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")

        day = request.POST.get("day")
        month = request.POST.get("month")
        year = request.POST.get("year")

        try:
            dob = datetime(int(year), int(month), int(day)).date()
        except:
            return render(request, 'registration/login.html', {
                'error': 'Invalid DOB',
                'days': range(1, 32),
                'years': range(1980, 2050)
            })

        try:
            student = Student.objects.get(mobile=mobile, dob=dob)
            request.session['student_id'] = student.id

            if not student.father_name:
                return redirect('complete_registration')

            return redirect('dashboard')

        except Student.DoesNotExist:
            return render(request, 'registration/login.html', {
                'error': 'Mobile or DOB incorrect',
                'days': range(1, 32),
                'years': range(1980, 2050)
            })

    # ✅ IMPORTANT FIX (days/years MUST be sent)
    return render(request, 'registration/login.html', {
        'days': range(1, 32),
        'years': range(1980, 2050)
    })


# ---------------- COMPLETE REGISTRATION ----------------
def complete_registration(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        student.father_name = request.POST.get("father_name")
        student.village = request.POST.get("village")
        student.post = request.POST.get("post")
        student.police_station = request.POST.get("police_station")
        student.district = request.POST.get("district")
        student.pincode = request.POST.get("pincode")
        student.seat_number = request.POST.get("seat_number")
        student.save()

        return redirect('dashboard')

    return render(request, 'complete_registration.html', {
        'student': student
    })


# ---------------- DASHBOARD (TODAY ONLY + PAYMENT + QR) ----------------
def dashboard(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    today = timezone.now().date()

    # ✅ ONLY TODAY attendance
    attendance, _ = Attendance.objects.get_or_create(
        student=student,
        date=today
    )

    # 🔥 payment alert (1-3 date only)
    show_payment_alert = (1 <= today.day <= 3 and not student.is_paid)

    # 🔥 last payment
    payment = Payment.objects.filter(student=student).order_by('-id').first()

    # 🔥 UPI LINK (multiple apps support)
    upi_link = (
        f"upi://pay?"
        f"pa=vikash@ybl"
        f"&pn=TBH Library"
        f"&am={student.payment_due or 100}"
        f"&cu=INR"
    )

    qr = qrcode.make(upi_link)
    buffer = BytesIO()
    qr.save(buffer)
    qr_img = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'dashboard.html', {
        'student': student,
        'attendance': attendance,
        'show_payment_alert': show_payment_alert,
        'payment': payment,
        'qr': qr_img
    })


# ---------------- CHECK IN ----------------
def check_in(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    attendance, _ = Attendance.objects.get_or_create(
        student=student,
        date=timezone.now().date()
    )

    # ✅ INDIA TIME FIX
    if attendance.check_in is None:
        attendance.check_in = timezone.localtime(timezone.now())
        attendance.save()

    return redirect('dashboard')


# ---------------- CHECK OUT ----------------
def check_out(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    attendance = Attendance.objects.filter(
        student=student,
        date=timezone.now().date()
    ).first()

    if attendance and attendance.check_out is None:
        attendance.check_out = timezone.localtime(timezone.now())
        attendance.save()

    return redirect('dashboard')


# ---------------- ADD STUDENT ----------------
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()

    return render(request, 'student_form.html', {'form': form})


# ---------------- PAYMENT PAGE ----------------
def payment_qr(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)

    upi_link = (
        f"upi://pay?"
        f"pa=vikash@ybl"
        f"&pn=TBH Library"
        f"&am={student.payment_due or 100}"
        f"&cu=INR"
    )

    qr = qrcode.make(upi_link)
    buffer = BytesIO()
    qr.save(buffer)

    img_str = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "payment_qr.html", {
        "qr": img_str,
        "student": student
    })