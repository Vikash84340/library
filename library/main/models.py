from django.db import models
from django.utils import timezone


# ---------------- STUDENT ----------------
class Student(models.Model):

    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, null=True, blank=True)

    mobile = models.CharField(max_length=15, unique=True)
    dob = models.DateField()

    village = models.CharField(max_length=100, null=True, blank=True)
    post = models.CharField(max_length=100, null=True, blank=True)
    police_station = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    seat_number = models.CharField(max_length=10, null=True, blank=True)

    payment_due = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ---------------- ATTENDANCE ----------------
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    date = models.DateField(default=timezone.now)

    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.date}"


# ---------------- PAYMENT ----------------
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    amount = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.status}"