from django import forms
from django.core import validators
from .models import Book

class BookCreateForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(
        required=True,
        widget=forms.Textarea, 
        validators=[validators.MinLengthValidator(5, 'Please enter at least 5 charactors')],
    )
    image = forms.ImageField() 

    class Meta:
        model = Book
        fields = ['title', 'description', 'image']