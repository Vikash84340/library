from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'dob': forms.SelectDateWidget(years=range(1980, 2050))
        }
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'father_name',
            'mobile',
            'dob',
            'village',
            'post',
            'police_station',
            'district',
            'pincode',
            'seat_number',
            'payment_due',
            'is_paid'
        ]        