from django import forms
from .models import Task, User, ContactMessage, Comment, IssuePost
from django.contrib.auth.forms import UserCreationForm


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'task_type', 'proof_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Cleaned up local park'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe what you did and its impact.'}),
            'task_type': forms.Select(attrs={'class': 'form-select'}),
            'proof_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'area'] # Added area


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message', 'email']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Add your comment here...'
            })
        }


class IssuePostForm(forms.ModelForm):
    class Meta:
        model = IssuePost
        fields = ['title', 'description', 'image', 'area', 'location_details', 'department', 'status'] # Added 'department'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Pothole on Main Street'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue in detail.'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Downtown, Sector 12'}), # Changed to TextInput for flexibility
            'location_details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., In front of City Hall'}),
            'department': forms.Select(attrs={'class': 'form-select'}), # Bootstrap select class
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
