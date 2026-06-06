from django import forms
from prac_app.models import*
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username','display_name','user_type','email','password1','password2']

class LoginForm(AuthenticationForm):
    pass

class RecruiterProfileForm(forms.ModelForm):

    class Meta:
        model = RecruiterProfile

        fields = [
            'company_name',
            'company_email',
            'company_website',
            'company_description',
            'company_logo'
        ]

class JobSeekerProfileForm(forms.ModelForm):

    class Meta:
        model = JobSeekerProfile

        fields = [
            'full_name',
            'skills',
            'bio',
            'profile_image',
            'resume'
        ]

class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'number_of_openings',
            'category',
            'job_description',
            'skills_set'
        ]