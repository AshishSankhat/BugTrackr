from django import forms
from django.contrib.auth.models import User
from accounts.models import userData
from django_recaptcha.fields import ReCaptchaField


class UserForm(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['username', 'email','password']


class UserprofileForm(forms.ModelForm):
    class Meta:
        model = userData
        fields = [
            'Door_no','street','city','state','zipcode','profile_pic'
        ]
    captcha = ReCaptchaField()


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username','email']

class update_details(forms.ModelForm):
    class Meta:
        model = userData
        fields = ['Door_no','street','city','state','zipcode','profile_pic']



class ForgotpasswordForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if username:
            try:
                User.objects.get(username=username)
                if password != confirm_password:
                    raise forms.ValidationError("Passwords do not match")
            except User.DoesNotExist:
                raise forms.ValidationError("Username does not exist")