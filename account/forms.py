from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password",
                                widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    """ 
    (методы clean_<field> вызываются при проверке form.is_valid вместе с clean)
    есть также общий метод clean, если его использовать, то он переопределит дефолтный.
    
    Django также предоставляет форму UserCreationForm, которая находится
    в django.contrib.auth.forms и очень похожа на эту.
    """

    # Метод валидации пароля 
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
     
    # Уже встроенная проверка
    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     if User.objects.filter(username=data).exists():
    #         raise forms.ValidationError('Username already in use.')
    #     return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                         .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
