from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from application.sap.models import (
    CommentedFeedback,
    FeedbackSettings,
    User,
)


text_validator = RegexValidator(r'[а-яА-Яa-zA-Z]',
                               'Text should contain letters')

telergam_channel_validator = RegexValidator(r'^@.*',
                                           'Telegram channel name must have "@" at the begining')

not_empty_validator = RegexValidator(r'^.*',
                                    'Fields must not be empty')


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


class FeedbackSettingsForm(forms.ModelForm):
    group_name = forms.CharField(
        validators=[not_empty_validator], 
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
    class_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Class type (e.g. lection, seminar and etc)',
        })
    )
    telegram_channel = forms.CharField(
        validators=[telergam_channel_validator], 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telegram channel (e.g. @group_channel)',
        })
    )
    feedback_type = forms.ChoiceField(
        choices=(("commented", "Commented"), ("estimated", "Estimated")),
        widget=forms.Select(attrs={
            'class': 'feedback-type',
        })
    )

    class Meta:
        model = FeedbackSettings
        fields = ['group_name', 'subject', 'class_type', 'telegram_channel', 'feedback_type']


class CommentedStatisticsForm(forms.Form):
    date = forms.DateField(
        widget=forms.TextInput(attrs={
            'id': 'date',
            'data-toggle':'datepicker',
            'placeholder': 'date',
            'autocomplete': 'off',
        }),
    )
    group_name = forms.CharField(
        validators=[not_empty_validator], 
        widget=forms.TextInput(attrs={
            'id': 'group_name',
            'class': 'form-control',
            'placeholder': 'Student group name',
        })
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'subject',
            'class': 'form-control',
            'placeholder': 'Subject name',
        })
    )
    class_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'class_type',
            'class': 'form-control',
            'placeholder': 'Class type',
        })
    )


class GroupAverageStatisticsForm(forms.Form):
    period_from = forms.DateField(
        widget=forms.TextInput(attrs={
            'id': 'from',
            'data-toggle':'datepicker',
            'placeholder': 'From',
            'autocomplete': 'off',
        }),
    )
    period_to = forms.DateField(
        widget=forms.TextInput(attrs={
            'id': 'to',
            'data-toggle':'datepicker',
            'placeholder': 'To',
            'autocomplete': 'off',
        }),
    )
    group_name = forms.CharField(
        validators=[not_empty_validator], 
        widget=forms.TextInput(attrs={
            'id': 'group_name',
            'class': 'form-control',
            'placeholder': 'Student group name',
        })
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'subject',
            'class': 'form-control',
            'placeholder': 'Subject name',
        })
    )
    class_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'class_type',
            'class': 'form-control',
            'placeholder': 'Class type',
        })
    )


class GroupDayInfoStatisticsForm(forms.Form):
    date = forms.DateField(
        widget=forms.TextInput(attrs={
            'id': 'date',
            'data-toggle':'datepicker',
            'placeholder': 'Date',
            'autocomplete': 'off',
        }),
    )
    group_name = forms.CharField(
        validators=[not_empty_validator], 
        widget=forms.TextInput(attrs={
            'id': 'group_name',
            'class': 'form-control',
            'placeholder': 'Student group name',
        })
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'subject',
            'class': 'form-control',
            'placeholder': 'Subject name',
        })
    )
    class_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'class_type',
            'class': 'form-control',
            'placeholder': 'Class type',
        })
    )
