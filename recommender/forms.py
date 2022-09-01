from tkinter import Widget
from django.forms import ModelForm, TextInput
from .models import Meal, MealRating, Tag


class CreateForm(ModelForm):
    class Meta:
        model = Meal
        fields = ('name', 'description', 'imageUrl', 'countryOfOrigin', 'tag')

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = 'form-control mt-2 mb-2 rounded text-dark-light'
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.all()


class DetailForm(ModelForm):
    class Meta:
        model = MealRating
        fields = ['rating']
        widgets = {
            "rating": TextInput(attrs={
                "type": "range",
                "max": 5,
                "min": 0,
                "step": 0.1
            })
        }
