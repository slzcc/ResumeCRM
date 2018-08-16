from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from repository.models import UserProfile
from repository import models


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class customUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', min_length=8,  max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password confirmation', min_length=8,  max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder': 'Password Confirmation'}))

    class Meta:
        model = UserProfile
        fields = ('email', 'name', 'phone', 'location', 'describe')
        widgets = {
            'email' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Email'}),
            'name' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Name'}),
            'phone' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'Phone'}),
            'location' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'ex: CN'}),
            'describe' : forms.Textarea(attrs={'class':"form-control", 'style': 'height: 125px'}),
        }
        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})
                # if field_name in admin_class.readonly_fields:
                #     filed_obj.widget.attrs.update({'disabled': 'true'})
                #     print("--new meta:",cls.Meta)

            #print(cls.Meta.exclude)
            return  ModelForm.__new__(cls)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class customUpdateUserPasswordForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', min_length=8,  max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password confirmation', min_length=8,  max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control", 'placeholder': 'Password Confirmation'}))
    
    class Meta:
        model = UserProfile
        fields = ('password',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class customUpdateUserInfoForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = UserProfile
        fields = ('email', 'name', 'phone', 'location','describe',)
        widgets = {
            'email' : forms.TextInput(attrs={'class':"form-control", 'readonly':'readonly'}),
            'name' : forms.TextInput(attrs={'class':"form-control", }),
            'phone' : forms.TextInput(attrs={'class':"form-control", }),
            'location' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'ex: CN'}),
            'describe' : forms.Textarea(attrs={'class':"form-control", 'style': 'height: 125px'}),
            # 'groups' : forms.SelectMultiple(attrs={'class':"form-control"}),

        }
        def __new__(cls, *args, **kwargs):
            # print("__new__",cls,args,kwargs)
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})
                # if field_name in admin_class.readonly_fields:
                #     filed_obj.widget.attrs.update({'disabled': 'true'})
                #     print("--new meta:",cls.Meta)

            #print(cls.Meta.exclude)
            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class customUpdateUserInfoForm_user(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = UserProfile
        fields = ('email', 'name', 'phone', 'location','describe', 'groups', 'is_active', 'is_staff',)
        widgets = {
            'email' : forms.TextInput(attrs={'class':"form-control", 'readonly':'readonly'}),
            'name' : forms.TextInput(attrs={'class':"form-control", }),
            'phone' : forms.TextInput(attrs={'class':"form-control", }),
            'location' : forms.TextInput(attrs={'class':"form-control", 'placeholder': 'ex: CN'}),
            'describe' : forms.Textarea(attrs={'class':"form-control", 'style': 'height: 125px'}),
            'groups' : forms.SelectMultiple(attrs={'class':"multi-select","data-plugin": "multiselect", "style": "position: absolute; left: -9999px"}),

        }
        def __new__(cls, *args, **kwargs):
            # print("__new__",cls,args,kwargs)
            for field_name in cls.base_fields:
                filed_obj = cls.base_fields[field_name]
                filed_obj.widget.attrs.update({'required':''})
                # if field_name in admin_class.readonly_fields:
                #     filed_obj.widget.attrs.update({'disabled': 'true'})
                #     print("--new meta:",cls.Meta)

            #print(cls.Meta.exclude)
            return  ModelForm.__new__(cls)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user