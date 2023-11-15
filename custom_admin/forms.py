from accounts.models import Cases, Certificates, User, UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as BaseUserChangeForm
import re
from django import forms


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
                             help_text="Required. Enter a valid email address")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',
                  'is_doctor', 'phone', 'clinic')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^01[0-2]\d{8}$', phone):
            raise forms.ValidationError(
                "Enter a valid Egyptian mobile phone number.")
        return phone


class UserChangeForm(BaseUserChangeForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'is_staff',
                  'is_superuser', 'is_doctor', 'phone', 'clinic']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['info', 'bio', 'profile_picture', 'contact']


CertificatesFormSet = forms.inlineformset_factory(
    UserProfile, Certificates, fields=('certificate',), extra=1)
CasesFormSet = forms.inlineformset_factory(
    UserProfile, Cases, fields=('case',), extra=1)
