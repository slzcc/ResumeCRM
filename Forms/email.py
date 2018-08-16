from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from repository.models import UserProfile
from repository import models
from django.contrib.auth.models import Group

class EmailCreationForm(forms.ModelForm):
    class Meta:
        model = models.Email
        fields = ('name', 'form_address', 'form_name', 'smtp_server', 'smtp_port','smtp_username','smtp_password','smtp_ssl')
        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control", 'placeholder': ''}),
            'form_address' : forms.TextInput(attrs={'class':"form-control", 'placeholder': ''}),
            'form_name' : forms.TextInput(attrs={'class':"form-control", 'placeholder': ''}),
            'smtp_server' : forms.TextInput(attrs={'class':"form-control", 'placeholder': ''}),
            'smtp_port' : forms.TextInput(attrs={'class':"form-control", 'placeholder': ''}),
            'smtp_username' : forms.TextInput(attrs={'class':"form-control", 'placeholder': ''}),
            'smtp_password' : forms.PasswordInput(attrs={'class':"form-control", 'placeholder': ''}),
            'smtp_ssl' : forms.CheckboxInput(attrs={'class':"form-control", 'placeholder': ''}),
        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        email = super().save(commit=False)
        if commit:
            email.save()
        return email