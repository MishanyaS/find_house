import datetime
from decimal import Decimal
import re
from django import forms
from find_house_app.models import Announcement, Category, AnnouncementImage, News, AnnouncementViewHistory, Comment, Favorite
from users_app.models import CustomUser
from chat_app.models import Chat, Message
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from admin_panel_app.models import Content


# region User forms
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'custom-form-control'}), required=False, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'custom-form-control'}), required=False, label="Confirm Password")
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone_number', 'birth_date', 'address', 'avatar', 'description', 'is_admin']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'custom-form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'custom-form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'custom-form-control'}),
            'password2' : forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'custom-form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'custom-form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'custom-form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '999999999', 'class': 'custom-form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'custom-form-control'}),
            'address': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Enter your Address'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'custom-form-control form-control'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 4, 'cols': 50, 'placeholder': 'Tell us something about yourself'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input',})
        }
        
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'password2' : 'Confirm Password',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'birth_date': 'Birth Date',
            'address': 'Address',
            'avatar': 'Avatar',
            'description': 'Description',
            'is_admin': 'Is Admin'
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
            raise ValidationError('<strong>Username</strong> max length is 255 symbols.')

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
        
        if not password:
            raise ValidationError(mark_safe('<strong>Password</strong> is required.'))

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

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        new_password = self.cleaned_data.get("new_password")
        if password and new_password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'custom-form-control'}), required=False, label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'custom-form-control'}), required=False, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'custom-form-control'}), required=False, label="Confirm New Password")
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'address', 'avatar', 'description', 'is_admin']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'custom-form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'custom-form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'custom-form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'custom-form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '999999999', 'class': 'custom-form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'custom-form-control'}),
            'address': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Enter your Address'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'custom-form-control form-control'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 4, 'cols': 50, 'placeholder': 'Tell us something about yourself'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input',})
        }
        
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'birth_date': 'Birth Date',
            'address': 'Address',
            'avatar': 'Avatar',
            'description': 'Description',
            'is_admin': 'Is Admin',
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

# region AnnouncementCreate forms
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'price', 'square', 'owner', 'category', 'status', 'address']
        exclude = ['views', 'date_added']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder' : 'Title'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'price': forms.NumberInput(attrs={'class': 'custom-form-control', 'placeholder' : 'Price'}),
            'square': forms.NumberInput(attrs={'class': 'custom-form-control', 'placeholder' : 'Square'}),
            'owner': forms.HiddenInput(),
            'category': forms.Select(attrs={'class': 'custom-form-select'}),
            'status': forms.Select(attrs={'class': 'custom-form-select'}),
            'address': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder' : 'Address'}),
        }

        labels = {
            'title': 'Title',
            'description': 'Description',
            'price': 'Price',
            'square': 'Square',
            'owner': 'Owner',
            'category': 'Category',
            'status': 'Status',
            'address': 'Address',
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].required = False
        self.fields['description'].required = False
        self.fields['price'].required = False
        self.fields['square'].required = False
        self.fields['category'].required = False
        self.fields['status'].required = False
        self.fields['address'].required = False
        
        if self.current_user:
            self.fields['owner'].queryset = CustomUser.objects.filter(id=self.current_user.id)
            self.fields['owner'].initial = self.current_user
                        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError(mark_safe('<strong>Title</strong> is required.'))
        
        if len(title) > 255:
            raise ValidationError(mark_safe('<strong>Title</strong> max length is 255 symbols.'))

        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError(mark_safe('<strong>Description</strong> is required.'))
        
        if len(description) > 5000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 5000 symbols.'))
        
        return description
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        
        if not price:
            raise ValidationError(mark_safe('<strong>Price</strong> is required.'))
        
        if price < 0:
            raise ValidationError(mark_safe('<strong>Price</strong> can not be less than 0.'))
        
        if not isinstance(price, Decimal):
            raise ValidationError(mark_safe('Invalid <strong>Price</strong> format. Please enter a valid Decimal.'))

        price_str = str(price).replace(',', '.')
        price_pattern = re.compile(r'^[1-9]\d{0,9}(\.\d{2})?$')
        if not price_pattern.match(price_str):
            raise ValidationError(mark_safe('Invalid <strong>Price</strong> format. Please enter a value with at least one digit before the dot and two digits after the dot.'))
        
        return price
    
    def clean_square(self):
        square = self.cleaned_data.get('square')
        
        if not square:
            raise ValidationError(mark_safe('<strong>Square</strong> is required.'))
        
        if square < 0:
            raise ValidationError(mark_safe('<strong>Square</strong> can not be less than 0.'))
        
        if square is int:
            raise ValidationError(mark_safe('<strong>Square</strong> have to be digit.'))
        
        return square
    
    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise ValidationError(mark_safe('<strong>Category</strong> is required.'))
        
        return category
    
    def clean_status(self):
        status = self.cleaned_data.get('status')

        if not status:
            raise ValidationError(mark_safe('<strong>Status</strong> is required.'))

        return status
    
    def clean_address(self):
        status = self.cleaned_data.get('address')

        if not status:
            raise ValidationError(mark_safe('<strong>Address</strong> is required.'))

        return status
# endregion

# region CarCreate forms
class AnnouncementImageForm(forms.ModelForm):
    class Meta:
        model = AnnouncementImage
        fields = ['announcement', 'image', 'description']
        exclude = ['date_added']

        widgets = {
            'announcement': forms.Select(attrs={'class': 'custom-form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'custom-form-control form-control'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter a description or caption for the image'}),
        }
        
        labels = {
            'announcement': 'Select Announcement',
            'image': 'Upload Image',
            'description': 'Image Description'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['announcement'].required = False
        self.fields['image'].required = False
        self.fields['description'].required = False
        
    def clean_announcement(self):
        announcement = self.cleaned_data.get('announcement')
        
        if not announcement:
            raise ValidationError(mark_safe('<strong>Announcement</strong> is required.'))
        
        return announcement
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if not image:
            raise ValidationError(mark_safe('<strong>Image</strong> is required.'))
        
        return image
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError(mark_safe('<strong>Description</strong> is required.'))
        
        if len(description) > 1000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 1000 symbols.'))
        
        return description
          
AnnouncementImageFormSet = inlineformset_factory(Announcement, AnnouncementImage, form=AnnouncementImageForm, extra=5, can_delete=True)
# endregion

# region Category forms
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        exclude = ['date_added']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter description'}),
        }
        
        labels = {
            'name': 'Name',
            'description': 'Description',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].required = False
        self.fields['description'].required = False
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError(mark_safe('<strong>Name</strong> is required.'))
        
        if len(name) > 255:
            raise ValidationError(mark_safe('<strong>Name</strong> max length is 255 symbols.'))
        
        return name
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError(mark_safe('<strong>Description</strong> is required.'))
        
        if len(description) > 1000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 1000 symbols.'))
        
        return description
# endregion

# region Favorite forms
class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['user', 'announcement', 'is_in_favorite']
        exclude = ['date_added',]
        
        widgets = {
            'user': forms.Select(attrs={'class': 'custom-form-control'}),
            'announcement': forms.Select(attrs={'class': 'custom-form-control'}),
            'is_in_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'user': 'Select User',
            'announcement': 'Select Announcement',
            'is_in_favorite': 'Is in Favorite',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['user'].required = False
        self.fields['announcement'].required = False
        self.fields['is_in_favorite'].required = False
        
    def clean_user(self):
        user = self.cleaned_data.get('user')
        
        if not user:
            raise ValidationError(mark_safe('<strong>User</strong> is required.'))
        
        return user
    
    def clean_announcement(self):
        announcement = self.cleaned_data.get('announcement')
        
        if not announcement:
            raise ValidationError(mark_safe('<strong>Announcement</strong> is required.'))
        
        return announcement
# endregion

# region NewsItem forms
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        exclude = ['views_count', 'date_added']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'custom-form-control', 'placeholder': 'Content', 'rows': 3}),
        }
        
        labels = {
            'title': 'Title',
            'content': 'Content',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].required = False
        self.fields['content'].required = False
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError(mark_safe('<strong>Title</strong> is required.'))
        
        if len(title) > 255:
            raise ValidationError(mark_safe('<strong>Title</strong> max length is 255 symbols.'))
        
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        
        if not content:
            raise ValidationError(mark_safe('<strong>Content</strong> is required.'))
        
        if len(content) > 5000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 5000 symbols.'))
                
        return content
# endregion

# region AnnouncementViewHistory forms
class AnnouncementViewHistoryForm(forms.ModelForm):
    class Meta:
        model = AnnouncementViewHistory
        fields = ['user', 'announcement',]
        exclude = ['date']
        
        widgets = {
            'user': forms.Select(attrs={'class': 'custom-form-control'}),
            'announcement': forms.Select(attrs={'class': 'custom-form-control'}),
        }

        labels = {
            'user': 'Select User',
            'announcement': 'Select Announcement',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['user'].required = False
        self.fields['announcement'].required = False
        
    def clean_user(self):
        user = self.cleaned_data.get('user')
        
        if not user:
            raise ValidationError(mark_safe('<strong>User</strong> is required.'))
        
        return user
    
    def clean_announcement(self):
        announcement = self.cleaned_data.get('announcement')
        
        if not announcement:
            raise ValidationError(mark_safe('<strong>Announcement</strong> is required.'))
        
        return announcement
# endregion

# region Comment forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['announcement', 'user', 'text']
        exclude = ['date_added']
        
        widgets = {
            'announcement': forms.Select(attrs={'class': 'custom-form-control'}),
            'user': forms.Select(attrs={'class': 'custom-form-control'}),
            'text': forms.Textarea(attrs={'class': 'custom-form-control', 'placeholder': 'Text', 'rows': 3}),
        }

        labels = {
            'announcement': 'Announcement',
            'user': 'User',
            'text': 'Text',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['announcement'].required = False
        self.fields['user'].required = False
        self.fields['text'].required = False
        
    def clean_announcement(self):
        announcement = self.cleaned_data.get('announcement')
        
        if not announcement:
            raise ValidationError(mark_safe('<strong>Announcement</strong> is required.'))
                
        return announcement
    
    def clean_user(self):
        user = self.cleaned_data.get('user')
        
        if not user:
            raise ValidationError(mark_safe('<strong>User</strong> is required.'))
                
        return user
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        
        if not text:
            raise ValidationError(mark_safe('<strong>Text</strong> is required.'))
        
        if len(text) > 1000:
            raise ValidationError(mark_safe('<strong>Text</strong> max length is 1000 symbols.'))
        
        return text
# endregion

# region Chats forms
class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['participants']
        exclude = ['date_added']
        
        widgets = {
            'participants': forms.SelectMultiple(attrs={'class': 'custom-form-control'}),
        }

        labels = {
            'participants': 'Participants',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['participants'].required = False
        
    def clean_participants(self):
        participants = self.cleaned_data.get('participants')
        
        if not participants:
            raise ValidationError(mark_safe('<strong>Participants</strong> is required.'))
                
        return participants
# endregion

# region Chats forms
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['chat', 'sender', 'content', 'is_deleted', 'is_edited']
        exclude = ['timestamp']
        
        widgets = {
            'chat': forms.Select(attrs={'class': 'custom-form-control'}),
            'sender': forms.Select(attrs={'class': 'custom-form-control'}),
            'content': forms.Textarea(attrs={'class': 'custom-form-control'}),
            'is_deleted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_edited': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'chat': 'Chat',
            'sender': 'Sender',
            'content': 'Content',
            'is_deleted': 'Is deleted',
            'is_edited': 'Is edited',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['chat'].required = False
        self.fields['sender'].required = False
        self.fields['content'].required = False
        self.fields['is_deleted'].required = False
        self.fields['is_edited'].required = False
        
    def clean_chat(self):
        chat = self.cleaned_data.get('chat')
        
        if not chat:
            raise ValidationError(mark_safe('<strong>Chat</strong> is required.'))
                
        return chat
    
    def clean_sender(self):
        sender = self.cleaned_data.get('sender')
        
        if not sender:
            raise ValidationError(mark_safe('<strong>Sender</strong> is required.'))
                
        return sender
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        
        if not content:
            raise ValidationError(mark_safe('<strong>Content</strong> is required.'))
        
        if len(content) > 1000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 1000 symbols.'))
                
        return content
# endregion

# region Content forms
class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['contacts_page_h5', 'contacts_page_text', 'contacts_page_address', 'contacts_page_telephone', 'contacts_page_email', 'footer_text']
        exclude = ['change_date']
        
        widgets = {
            'contacts_page_h5': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Enter contacts page h5'}),
            'contacts_page_text': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter contacts page text'}),
            'contacts_page_address': forms.TextInput(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter contacts page address'}),
            'contacts_page_telephone': forms.TextInput(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter contacts page telephone'}),
            'contacts_page_email': forms.EmailInput(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter contacts page email'}),
            'footer_text': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter footer text'}),
        }
        
        labels = {
            'contacts_page_h5': 'Contacts Page h5',
            'contacts_page_text': 'Contacts Page Text',
            'contacts_page_address': 'Contacts Page Address',
            'contacts_page_telephone': 'Contacts Page Telephone',
            'contacts_page_email': 'Contacts Page Email',
            'footer_text': 'Footer Text',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['contacts_page_h5'].required = False
        self.fields['contacts_page_text'].required = False
        self.fields['contacts_page_address'].required = False
        self.fields['contacts_page_telephone'].required = False
        self.fields['contacts_page_email'].required = False
        self.fields['footer_text'].required = False
        
    def clean_contacts_page_h5(self):
        contacts_page_h5 = self.cleaned_data.get('contacts_page_h5')
        
        if not contacts_page_h5:
            raise ValidationError(mark_safe('<strong>Contacts Page h5</strong> is required.'))
        
        if len(contacts_page_h5) > 255:
            raise ValidationError(mark_safe('<strong>Contacts Page h5</strong> max length is 255 symbols.'))
        
        return contacts_page_h5
    
    def clean_contacts_page_text(self):
        contacts_page_text = self.cleaned_data.get('contacts_page_text')
        
        if not contacts_page_text:
            raise ValidationError(mark_safe('<strong>Contacts Page Text</strong> is required.'))
        
        if len(contacts_page_text) > 1000:
            raise ValidationError(mark_safe('<strong>Contacts Page Text</strong> max length is 1000 symbols.'))
        
        return contacts_page_text
    
    def clean_contacts_page_address(self):
        contacts_page_address = self.cleaned_data.get('contacts_page_address')
        
        if not contacts_page_address:
            raise ValidationError(mark_safe('<strong>Contacts Page Address</strong> is required.'))
        
        if len(contacts_page_address) > 1000:
            raise ValidationError(mark_safe('<strong>Contacts Page Address</strong> max length is 1000 symbols.'))
        
        return contacts_page_address
    
    def clean_contacts_page_telephone(self):
        contacts_page_telephone = self.cleaned_data.get('contacts_page_telephone')
        
        if not contacts_page_telephone:
            raise ValidationError(mark_safe('<strong>Contacts Page Telephone</strong> is required.'))
                
        if not contacts_page_telephone.isdigit():
            raise ValidationError(mark_safe('<strong>Contacts Page Telephone</strong> should contain only digits.'))

        if len(contacts_page_telephone) != 10:
            raise ValidationError(mark_safe('<strong>Contacts Page Telephone</strong> should be 10 digits long.'))
        
        return contacts_page_telephone
    
    def clean_contacts_page_email(self):
        contacts_page_email = self.cleaned_data.get('contacts_page_email')
        
        if not contacts_page_email:
            raise ValidationError(mark_safe('<strong>Contacts Page Email</strong> is required.'))
                
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_pattern.match(contacts_page_email):
            raise ValidationError(mark_safe('Invalid <strong>Contacts Page Email</strong> format.'))
        
        return contacts_page_email
    
    def clean_footer_text(self):
        footer_text = self.cleaned_data.get('footer_text')
        
        if not footer_text:
            raise ValidationError(mark_safe('<strong>Footer Text</strong> is required.'))
        
        if len(footer_text) > 1000:
            raise ValidationError(mark_safe('<strong>Footer Text</strong> max length is 1000 symbols.'))
        
        return footer_text
# endregion
