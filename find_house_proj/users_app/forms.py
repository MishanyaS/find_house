import re
from django import forms
from users_app.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# region Registration forms
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Enter Password'), 'class': 'custom-form-control'}), label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password'), 'class': 'custom-form-control'}), label=_('Confirm Password'))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone_number', 'birth_date', 'address', 'avatar', 'description', 'is_admin']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': _('Username'), 'class': 'custom-form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': _('Email Address'), 'class': 'custom-form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': _('Enter Password'), 'class': 'custom-form-control'}),
            'password2' : forms.PasswordInput(attrs={'placeholder': _('Confirm Password'), 'class': 'custom-form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': _('First Name'), 'class': 'custom-form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Last Name'), 'class': 'custom-form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '999999999', 'class': 'custom-form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'custom-form-control'}),
            'address': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': _('Enter your Address')}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'custom-form-control form-control'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 4, 'cols': 50, 'placeholder': _('Tell us something about yourself')}),
            'is_admin': forms.HiddenInput(attrs={'class': 'form-check-input',})
        }
        
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password': _('Password'),
            'password2' : _('Confirm Password'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone_number': _('Phone Number'),
            'birth_date': _('Birth Date'),
            'address': _('Address'),
            'avatar': _('Avatar'),
            'description': _('Description'),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['password2'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone_number'].required = False
        self.fields['birth_date'].required = False
        self.fields['address'].required = False
        self.fields['description'].required = False
        self.fields['is_admin'].required = False
        
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise ValidationError(mark_safe('<strong>Username</strong> is required.'))
        
        if len(username) > 255:
            raise ValidationError(mark_safe('<strong>Username</strong> max length is 255 symbols.'))

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError(mark_safe('<strong>Email</strong> is required.'))
                
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(email):
            raise ValidationError(mark_safe('Invalid <strong>Email</strong> format.'))
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise ValidationError(mark_safe('<strong>Password</strong> is required.'))

        return password
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise ValidationError(mark_safe('<strong>Confirm Password</strong> is required.'))
        
        if password != password2:
            raise ValidationError(mark_safe('<strong>Passwords</strong> do not match.'))

        return password2
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise ValidationError(mark_safe('<strong>First Name</strong> is required.'))
        
        if len(first_name) > 255:
            raise ValidationError(mark_safe('<strong>First Name</strong> max length is 255 symbols.'))

        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise ValidationError(mark_safe('<strong>Last Name</strong> is required.'))
        
        if len(last_name) > 255:
            raise ValidationError(mark_safe('<strong>Last Name</strong> max length is 255 symbols.'))

        return last_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number:
            raise ValidationError(mark_safe('<strong>Phone Number</strong> is required.'))
                
        if not phone_number.isdigit():
            raise ValidationError(mark_safe('<strong>Phone Number</strong> should contain only digits.'))

        if len(phone_number) != 10:
            raise ValidationError(mark_safe('<strong>Phone Number</strong> should be 10 digits long.'))
        
        return phone_number
        
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if not birth_date:
            raise ValidationError(mark_safe('<strong>Birth Date</strong> is required.'))
        
        if birth_date.year < 1900:
            raise ValidationError(mark_safe('<strong>Birth Date</strong> can not be less than 1900.'))
        
        if birth_date > datetime.date.today().replace(year=datetime.date.today().year - 18):
            raise ValidationError(mark_safe('You are <strong>under 18</strong> years old.'))

        return birth_date
    
    def clean_address(self):
        address = self.cleaned_data.get('address')

        if not address:
            raise ValidationError(mark_safe('<strong>Address</strong> is required.'))
        
        if len(address) > 255:
            raise ValidationError('Address max length is 255 symbols.')

        return address
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError(mark_safe('<strong>Description</strong> is required.'))
        
        if len(description) > 1000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 1000 symbols.'))
        
        return description

    # Handling password hashing
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
# endregion

# region EditUser forms
class EditUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'custom-form-control'}), required=False, label=_('Old Password'))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'custom-form-control'}), required=False, label=_('New Password'))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'custom-form-control'}), required=False, label=_('Confirm New Password'))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'address', 'avatar', 'description', 'is_admin']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': _('Username'), 'class': 'custom-form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': _('Email Address'), 'class': 'custom-form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': _('First Name'), 'class': 'custom-form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Last Name'), 'class': 'custom-form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '999999999', 'class': 'custom-form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'custom-form-control'}),
            'address': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': _('Enter your Address')}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'custom-form-control form-control'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 4, 'cols': 50, 'placeholder': _('Tell us something about yourself')}),
            'is_admin': forms.HiddenInput(attrs={'class': 'form-check-input',})
        }
        
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone_number': _('Phone Number'),
            'birth_date': _('Birth Date'),
            'address': _('Address'),
            'avatar': _('Avatar'),
            'description': _('Description'),
            'is_admin': _('Is Admin'),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['old_password'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone_number'].required = False
        self.fields['birth_date'].required = False
        self.fields['address'].required = False
        self.fields['description'].required = False
        self.fields['is_admin'].required = False
        
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise ValidationError(mark_safe('<strong>Username</strong> is required.'))
        
        if len(username) > 255:
            raise ValidationError(mark_safe('<strong>Username</strong> max length is 255 symbols.'))

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError(mark_safe('<strong>Email</strong> is required.'))
                
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(email):
            raise ValidationError(mark_safe('Invalid <strong>Email</strong> format.'))
        return email
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if self.cleaned_data.get('new_password1') or self.cleaned_data.get('new_password2'):
            if not old_password:
                raise ValidationError(mark_safe('<strong>Old Password</strong> is required.'))

        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        
        if self.cleaned_data.get('old_password') or self.cleaned_data.get('new_password2'):
            if not new_password1:
                raise ValidationError(mark_safe('<strong>New Password1</strong> is required.'))

        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        
        if not self.cleaned_data.get('old_password') and new_password1 and new_password2:
            if not new_password2:
                raise ValidationError(mark_safe('<strong>Confirm New Password2</strong> is required.'))

            if new_password1 != new_password2:
                raise ValidationError(mark_safe('<strong>Passwords</strong> do not match.'))

        return new_password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise ValidationError(mark_safe('<strong>First Name</strong> is required.'))
        
        if len(first_name) > 255:
            raise ValidationError(mark_safe('<strong>First Name</strong> max length is 255 symbols.'))

        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise ValidationError(mark_safe('<strong>Last Name</strong> is required.'))
        
        if len(last_name) > 255:
            raise ValidationError(mark_safe('<strong>Last Name</strong> max length is 255 symbols.'))

        return last_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number:
            raise ValidationError(mark_safe('<strong>Phone Number</strong> is required.'))
                
        if not phone_number.isdigit():
            raise ValidationError(mark_safe('<strong>Phone Number</strong> should contain only digits.'))

        if len(phone_number) != 10:
            raise ValidationError(mark_safe('<strong>Phone Number</strong> should be 10 digits long.'))
        
        return phone_number
        
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if not birth_date:
            raise ValidationError(mark_safe('<strong>Birth Date</strong> is required.'))
        
        if birth_date.year < 1900:
            raise ValidationError(mark_safe('<strong>Birth Date</strong> can not be less than 1900.'))
        
        if birth_date > datetime.date.today().replace(year=datetime.date.today().year - 18):
            raise ValidationError(mark_safe('You are <strong>under 18</strong> years old.'))

        return birth_date
    
    def clean_address(self):
        address = self.cleaned_data.get('address')

        if not address:
            raise ValidationError(mark_safe('<strong>Address</strong> is required.'))
        
        if len(address) > 255:
            raise ValidationError(mark_safe('<strong>Address</strong> max length is 255 symbols.'))

        return address
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError(mark_safe('<strong>Description</strong> is required.'))
        
        if len(description) > 1000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 1000 symbols.'))
        
        return description
    
    def save(self, commit=True):
        user = super().save(commit=False)
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get('new_password2') 
        if old_password and new_password1 and new_password2:
            user.set_password(new_password1)
        if commit:
            user.save()
        return user
# endregion

# region Login forms
class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), max_length=150, widget=forms.TextInput(attrs={'placeholder': _('Username'), 'class': 'custom-form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'placeholder': _('Enter Password'), 'class': 'custom-form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].required = False
        self.fields['password'].required = False
        self.fields['username'].widget.attrs.update({'class': 'custom-form-control', 'placeholder': _('Username')})
        self.fields['password'].widget.attrs.update({'class': 'custom-form-control', 'placeholder': _('Enter Password')})
        
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise ValidationError(mark_safe('<strong>Username</strong> is required.'))
        
        if len(username) > 255:
            raise ValidationError(mark_safe('<strong>Username</strong> max length is 255 symbols.'))

        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')

        if not password:
            raise ValidationError(mark_safe('<strong>Password</strong> is required.'))
        
        # Check password match in db
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(mark_safe('Invalid <strong>Password</strong>.'))

        return password
# endregion

# region CustomPasswordReset forms
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'custom-form-control', 'placeholder': _('Email')}),)
    
    class Meta:
        model = CustomUser
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].required = False
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError(mark_safe('<strong>Email</strong> is required.'))
                
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(email):
            raise ValidationError(mark_safe('Invalid <strong>Email</strong> format.'))
        
        return email
# endregion
