from django.contrib import admin
from .models import Tag, Meal, MealRating
# Register your models here.

admin.site.register(Tag)
admin.site.register(Meal)
admin.site.register(MealRating)
