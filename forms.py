from django import forms
from .models import Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={'rows':3, 'class':'form-control', 'placeholder':'What is happening?'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add bootstrap classes to fields
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
