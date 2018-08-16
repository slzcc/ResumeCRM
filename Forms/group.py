from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from repository.models import UserProfile
from repository import models
from django.contrib.auth.models import Group

class GroupCreationFormAll(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control", }),
        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        return group

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control", }),
        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        return group