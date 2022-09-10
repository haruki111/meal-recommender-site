from recommender.models import Meal, MealRating
from accounts.models import CustomUser
import random

meals = Meal.objects.all()
print(meals)

for meal in meals:
    users = CustomUser.objects.all()
    for user in users:
        if meal.user != user:
            rating = random.randint(10, 50) / 10
            mealRating = MealRating(user=user, meal=meal, rating=rating)
            mealRating.save()
