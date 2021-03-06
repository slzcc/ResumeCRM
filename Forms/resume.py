from django import forms
from repository import models
from django.forms import fields

class ResumeSourceFrom(forms.ModelForm):

    class Meta:
        model = models.ResumeSource
        fields = ('name',)

        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Name'}),
        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        ResumeSource = super().save(commit=False)
        if commit:
            ResumeSource.save()
        return ResumeSource


class ResumeTemplateFrom(forms.ModelForm):

    class Meta:
        model = models.ResumeTemplate
        fields = ('name', 'url',)

        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Name'}),
            'url' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Name'}),
        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        ResumeTemplate = super().save(commit=False)
        if commit:
            ResumeTemplate.save()
        return ResumeTemplate

class ResumeBaseInfoFrom(forms.Form):
    username = fields.CharField(
        max_length=16,
        min_length=6,
        required=True,
    )

    phone = fields.IntegerField(
        required=True,
    )

class ResumeInfoFrom(forms.ModelForm):

    class Meta:
        model = models.ResumeInfo
        fields = (
            'username', 
            'email', 
            'phone', 
            'high', 
            'age',
            'gender', 
            'marital_status', 
            'birthday', 
            'place_residence', 
            'language', 
            'nation', 
            'degree', 
            'graduated_school', 
            'professional', 
            'learning_type', 
            'jobs', 
            'job_addr', 
            'current_situation',
            'nature_work',
            'marital_status',
            'work_time',
            'salary',
            'duty_time',
            'old_jobs',
            'old_company',
            'resume_source',
            'track_progress',
            'upload_user',
            'agent',
            'zh_filename',
            'en_filename',
            'create_time',
            'cnterview_time',
        )

        widgets = {
            'username' : forms.TextInput(attrs={'class':"form-control-plaintext", "style":"display:block", "disabled": "disabled"}),
            'email' : forms.EmailInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'phone' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'high' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'age' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'gender' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'marital_status' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'birthday' : forms.DateInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'place_residence' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'language' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'nation' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'degree' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'graduated_school' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'professional' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'learning_type' : forms.TextInput(attrs={'class':"form-control-plaintext","disabled": "disabled" }),
            'jobs' : forms.TextInput(attrs={'class':"form-control-plaintext","disabled": "disabled" }),
            'job_addr' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'current_situation' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'nature_work' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'marital_status' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'work_time' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'salary' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'duty_time' : forms.DateInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'old_jobs' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'old_company' : forms.TextInput(attrs={'class':"form-control-plaintext", "disabled": "disabled"}),
            'zh_filename' : forms.Select(attrs={'class':"form-control", "disabled": "true", "id": "attachmentName",}),
            'en_filename' : forms.Select(attrs={'class':"form-control", "disabled": "true",}),

        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':'', "disabled": "disabled"})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        ResumeInfo = super().save(commit=False)
        if commit:
            ResumeInfo.save()
        return ResumeInfo