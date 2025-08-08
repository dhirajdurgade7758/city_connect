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


# from django import forms
# from .models import IssuePost

# class IssuePostForm(forms.ModelForm):
#     class Meta:
#         model = IssuePost
#         fields = ['title', 'description', 'image', 'area']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issue title'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue'}),
#             'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter area'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }


# from .models import Comment

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
#         widgets = {
#             'text': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 2,
#                 'placeholder': 'Add a comment...'
#             })
#         }
from django import forms
from .models import Comment, IssuePost

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
        fields = ['title', 'description', 'image', 'area', 'location_details', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }