from django import forms
from django.forms import ModelForm
from allauth.account.forms import SignupForm, LoginForm
from .models import CustomUser


class SignupUserForm(SignupForm):
    user_name = forms.CharField(max_length=30, label='ユーザーネーム')

    class Meta:
        model = CustomUser
        if CustomUser.USERNAME_FIELD == 'email':
            fields = ['email', ]
        else:
            fields = ['username', 'email', ]

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.user_name = self.cleaned_data['user_name']
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LoginUserForm(LoginForm):
    class Meta:
        model = CustomUser
        if CustomUser.USERNAME_FIELD == 'email':
            fields = ['email', ]
        else:
            fields = ['username', 'email', ]


class ProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_name', 'icon']
