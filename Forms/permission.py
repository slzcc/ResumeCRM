from django import forms
from repository import models
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.utils import ProgrammingError


class wrong_class(object):
    id = ""

try:
    content_type = ContentType.objects.get_for_model(models.SystemPermission)
except :
    content_type = wrong_class()


class PermissionCreationForm(forms.ModelForm):

    class Meta:
        model = Permission
        fields = ('name','codename', 'content_type',)
        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control", }),
            'codename' : forms.TextInput(attrs={'class':"form-control", "placeholder": "ex: AppName.CodeName",}),
            'content_type' : forms.TextInput(attrs={'class':"form-control", "value": content_type.id}),

        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        permission = super().save(commit=False)
        if commit:
            permission.save()
        return permission


class SystemPermissionCreationForm(forms.ModelForm):

    class Meta:
        model = models.SystemPermission
        fields = ('url', 'per_method','describe', 'permissions','argument_list','name',)
        widgets = {
            'name' : forms.TextInput(attrs={'class':"form-control", }),
            # 'permissions' : forms.Select(attrs={'class':"form-control", }),
            'permissions' : forms.TextInput(attrs={'class':"form-control", 'readonly':'readonly'}),
            'url' : forms.Select(attrs={'class':"form-control"}),
            # 'url' : forms.TextInput(attrs={'class':"form-control", }),
            'per_method' : forms.Select(attrs={'class': "form-control select2 select2-hidden-accessible"}),
            'argument_list' : forms.Textarea(attrs={'class':"form-control",'style': 'height: 125px'}),
            'describe' : forms.Textarea(attrs={'class':"form-control", 'style': 'height: 125px'}),

        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})

            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        permissions = super().save(commit=False)
        if commit:
            permissions.save()
        return permissions