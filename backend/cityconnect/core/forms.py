from django import forms
from .models import Report
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from .models import User

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'category', 'description', 'image', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., MG Road, Pune'}),
        }



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type', 'proof_image']




class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message', 'email']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


