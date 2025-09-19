from django import forms
from .models import Job, ClientCompany, ServiceType, EngineerProfile, JobNote, TimeLog
from django import forms
from .models import EngineerProfile, Skill

# forms.py
from django import forms

class EngineerCSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'service_type', 'client', 'client_contact',
            'assigned_engineer', 'priority', 'scheduled_date', 'estimated_duration',
            'location', 'latitude', 'longitude'
        ]
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estimated_duration': forms.NumberInput(attrs={'placeholder': 'Duration in minutes'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter clients to only active ones
        self.fields['client'].queryset = ClientCompany.objects.filter(is_active=True)
        
        # Filter engineers to only available ones
        self.fields['assigned_engineer'].queryset = EngineerProfile.objects.filter(is_available=True)
        
        # Make some fields optional
        self.fields['client_contact'].required = False
        self.fields['assigned_engineer'].required = False
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False




class JobNoteForm(forms.ModelForm):
    class Meta:
        model = JobNote
        fields = ['note_type', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your notes here...'}),
        }

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['start_time', 'end_time', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe the work done...'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("End time must be after start time")
        
        return cleaned_data
    


class EngineerProfileForm(forms.ModelForm):
    class Meta:
        model = EngineerProfile
        fields = [
            'employee_id', 'skills', 'skill_level', 'hourly_rate', 
            'max_hours_per_week', 'is_available'
        ]
        widgets = {
            'skills': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.all()
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import EngineerProfile, Skill

# Get the custom user model
CustomUser = get_user_model()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import EngineerProfile, Skill

# Get the custom user model
CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = 'engineer'  # Set default role to engineer
        
        if commit:
            user.save()
        return user

class EngineerProfileForm(forms.ModelForm):
    class Meta:
        model = EngineerProfile
        fields = [
            'employee_id', 'skills', 'skill_level', 'hourly_rate', 
            'max_hours_per_week', 'is_available'
        ]
        widgets = {
            'skills': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.all()

from django import forms
from .models import JobNote, Expense

class JobNoteForm(forms.ModelForm):
    class Meta:
        model = JobNote
        fields = ['note_type', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your notes here...'}),
        }

class VoiceNoteForm(forms.ModelForm):
    audio_file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': 'audio/*'}),
        label="Voice Recording"
    )
    
    class Meta:
        model = JobNote
        fields = ['content', 'audio_file']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a description for this recording...'}),
        }

class ImageNoteForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'accept': 'image/*', 'capture': 'camera'}),
        label="Photo"
    )
    
    class Meta:
        model = JobNote
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a description for this photo...'}),
        }

class ExpenseForm(forms.ModelForm):
    receipt = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'accept': 'image/*', 'capture': 'camera'}),
        label="Receipt Photo"
    )
    
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'receipt', 'date_incurred']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe the expense...'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'date_incurred': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].required = True