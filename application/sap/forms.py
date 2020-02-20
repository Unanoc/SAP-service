from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from application.sap.models import (
    CommentedFeedback,
    CommentedFeedbackSettings,
    User,
)


text_validator = RegexValidator(r'[а-яА-Яa-zA-Z]',
                               'Text should contain letters')

student_group_validator = RegexValidator(r'^[а-яА-Я]{1,4}\d{0,2}\-\d{1,3}[а-яА-Я]?$',
                                        'Wrong student group format')

telergam_channel_validator = RegexValidator(r'^@.*',
                                        'Telegram channel name must have "@" at the begining')

comment_feedback_validator = RegexValidator(r'^.*',
                                        'Comment must not be empty')


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        validators=[text_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': 1,
            'maxlength': 30,
            'placeholder': 'First name',
        })
    )

    last_name = forms.CharField(
        validators=[text_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': 1,
            'maxlength': 30,
            'placeholder': 'Last name',
        })
    )

    username = forms.CharField(
        validators=[text_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': 1,
            'maxlength': 30,
            'placeholder': 'Username',
        })
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))

    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password confirmation',
    }))


    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise ValidationError("Password and Confirm password does not match")
        return cleaned_data


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 1,
        'maxlength': 30,
        'placeholder': 'Username',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise ValidationError("Sorry, that login or password is invalid. Please try again.")
        return self.cleaned_data


    class Meta:
        model = User
        fields = ['username', 'password']


class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(
        validators=[text_validator], 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': 1,
            'maxlength': 30,
            'placeholder': 'First name',
        })
    )

    last_name = forms.CharField(
        validators=[text_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': 1,
            'maxlength': 30,
            'placeholder': 'Last name',
        })
    )

    username = forms.CharField(
        validators=[text_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'minlength': 1,
            'maxlength': 30,
            'placeholder': 'Username',
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'upload']


class CommentedFeedbackSettingsForm(forms.ModelForm):
    group_name = forms.CharField(
        validators=[student_group_validator], 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Student group name',
        })
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject name',
        })
    )

    telegram_channel = forms.CharField(
        validators=[telergam_channel_validator], 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telegram channel',
        })
    )

    class Meta:
        model = CommentedFeedbackSettings
        fields = ['group_name', 'subject', 'telegram_channel']


class CommentedFeedbackForm(forms.ModelForm):
    text = forms.CharField(
        validators=[comment_feedback_validator], 
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your comment about passed class',
        })
    )

    class Meta:
        model = CommentedFeedback
        fields = ['text']