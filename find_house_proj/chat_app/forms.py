from django import forms
from chat_app.models import Message
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# region Comment forms
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content',]
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'custom-form-control', 'placeholder': 'Content', 'rows': '3'}),
        }
        
        labels = {
            'content': 'Message',
        }
        
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        
        self.fields['content'].required = False
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        
        if not content:
            raise ValidationError(mark_safe('<strong>Content</strong> is required.'))
        
        if len(content) > 1000:
            raise ValidationError(mark_safe('<strong>Description</strong> max length is 1000 symbols.'))
                
        return content

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.sender = self.current_user
        if commit:
            instance.save()
        return instance
# endregion
