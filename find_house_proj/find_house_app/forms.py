from decimal import Decimal
import re
from django import forms
from find_house_app.models import Announcement, Category, AnnouncementImage, News, AnnouncementViewHistory, Comment
from users_app.models import CustomUser
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# region AnnouncementImage forms
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
# endregion

# region Category forms
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description',]
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

# region Announcement forms
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'price', 'square', 'owner', 'category', 'status', 'address']
        exclude = ['views', 'date_added']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder' : 'Title'}),
            'description': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Enter a description'}),
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
            'address': 'Address'
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

AnnouncementImageFormSet = inlineformset_factory(Announcement, AnnouncementImage, form=AnnouncementImageForm, extra=5, can_delete=True)
# endregion

# region News forms
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        exclude = ['date_added']
        
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
        fields = ['user', 'announcement']
        exclude = ['date']
        
        widgets = {
            'user': forms.Select(attrs={'class': 'custom-form-select'}),
            'announcement': forms.Select(attrs={'class': 'custom-form-select'}),
        }
        
        labels = {
            'user': 'User',
            'announcement': 'Announcement Viewed',
        }
# endregion

# region Comment forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
        widgets = {
            'text': forms.Textarea(attrs={'class': 'custom-form-control', 'rows': 3, 'placeholder': 'Comment'}),
        }
        
        labels = {
            'text': 'Comment',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['text'].required = False
        
    def clean_text(self):
        text = self.cleaned_data.get('text')
        
        if not text:
            raise ValidationError(mark_safe('<strong>Comment</strong> is required.'))
        
        if len(text) > 1000:
            raise ValidationError(mark_safe('<strong>Comment</strong> max length is 1000 symbols.'))
        
        return text
# endregion

