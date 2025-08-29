from django import forms
from .models import Jobseeker
from .models import Job,Company

class JobseekerForm(forms.ModelForm):
    class Meta:
        model = Jobseeker
        fields = ['full_name', 'skills','email_id', 'resume','experience','mobile']


from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company']  # No posted_by here
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'company': forms.Select(attrs={'class': 'form-control'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'website']