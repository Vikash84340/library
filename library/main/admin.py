from django.contrib import admin
from .models import Student, Attendance, Payment

# Student admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'is_paid', 'payment_due')
    search_fields = ('name', 'mobile')

# Attendance admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'check_in', 'check_out')
    list_filter = ('date',)

# Payment admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__name', 'student__mobile')
# Register your models here.
