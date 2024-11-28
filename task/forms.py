from django import forms
from .models import Task
from datetime import date


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        labels = {
            "title": "Заголовок",
            "description": "Опис",
            "due_date": "Термін виконання",
        }


    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < date.today():
            raise forms.ValidationError("Дата виконання не може бути в минулому.")
        return due_date
