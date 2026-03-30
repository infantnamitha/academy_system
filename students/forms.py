"""
Students App - Forms
Form validation for adding/editing students
"""
from django import forms
from .models import Student, Course


class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ['name', 'phone', 'email', 'course', 'fees', 'fees_paid']
        widgets = {
            'name':      forms.TextInput(attrs={'placeholder': 'Full name', 'class': 'form-input'}),
            'phone':     forms.TextInput(attrs={'placeholder': '10-digit mobile number', 'class': 'form-input'}),
            'email':     forms.EmailInput(attrs={'placeholder': 'email@example.com (optional)', 'class': 'form-input'}),
            'course':    forms.Select(attrs={'class': 'form-input'}),
            'fees':      forms.NumberInput(attrs={'placeholder': 'Total fees (₹)', 'class': 'form-input', 'min': '0'}),
            'fees_paid': forms.NumberInput(attrs={'placeholder': 'Amount paid so far (₹)', 'class': 'form-input', 'min': '0'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        # Remove spaces/dashes for validation
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) < 10:
            raise forms.ValidationError('Phone number must have at least 10 digits.')
        return phone

    def clean(self):
        cleaned = super().clean()
        fees      = cleaned.get('fees', 0)
        fees_paid = cleaned.get('fees_paid', 0)
        if fees_paid and fees and fees_paid > fees:
            raise forms.ValidationError('Fees paid cannot be more than total fees.')
        return cleaned
