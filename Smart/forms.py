from django import forms
from .models import TodoItem

class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Add new task...',
                'class': 'form-control',
                'autocomplete': 'off'
            })
        }