from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Meal, Tag, MealRating
from .forms import CreateForm, DetailForm
from django.http import JsonResponse, HttpResponseServerError
from django.urls import reverse_lazy
import json
from django.db.models import Avg


class IndexView(TemplateView):
    template_name = 'index.html'


class MealCreateView(LoginRequiredMixin, FormView):
    template_name = 'recommender/create.html'
    form_class = CreateForm
    success_url = reverse_lazy('recommender:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()

        return context

    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = self.request.user
        data.save()
        tag_list = self.request.POST.get('tag').split(",")

        if tag_list:
            for tag in tag_list:
                data.tag.add(
                    Tag.objects.get(id=tag))

        form.save_m2m()
        return super().form_valid(form)


class HistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'recommender/history.html'
    model = Meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["recentlyAdded"] = Meal.objects.filter(user=self.request.user).order_by(
            '-dateAdded')[0:5]

        context["likeMeals"] = MealRating.objects.select_related("meal").filter(
            user=self.request.user)[0:5]

        return context


class MealDetail(DetailView):
    template_name: str = 'recommender/detail.html'
    model = Meal
    context_object_name = "meal"


def index_axios(request):
    if request.method == "GET":
        meals = Meal.objects.all().order_by('-dateAdded')[0:6]
        tags = Tag.objects.all()

        results = {'meals': get_meal_results(meals)}
        results.update({'tags': {'name': [tag.name for tag in tags],
                                 'id': [tag.pk for tag in tags]}})
        results.update({'mealsNum': Meal.objects.all().count()})
        results.update({'nowOrder': 1})

        if request.user.is_authenticated:
            recommendMeals = Meal.objects.exclude(
                user=request.user).order_by("?")[:5]
            test = sorted(
                Meal.objects.all(), key=lambda meal: meal.avgRating(), reverse=True)

            results.update({'recommended': get_meal_results(recommendMeals)})
        else:
            results.update({'recommended': []})

        return JsonResponse(results, safe=False)

    if request.method == "POST":
        selectChips = json.loads(request.POST.get("selectChips"))
        rangeMeals = json.loads(request.POST.get("rangeMeals"))
        orderBy = json.loads(request.POST.get("orderBy"))

        sl = slice(6 * (rangeMeals-1), 6 * rangeMeals)

        meals = []
        # All選択時
        if selectChips[0] == 0:
            meals = Meal.objects.all()
        else:
            meals = Meal.objects.filter(tag=selectChips[0])

            # ２個以上chip選択
            if len(selectChips) >= 2:
                for selectChip in selectChips[1:]:
                    meals = meals.filter(tag=selectChip)

        mealsNum = 0

        if orderBy == 'avgRating':
            meals = sorted(
                meals, key=lambda meal: meal.avgRating(), reverse=True)
            mealsNum = len(meals)
        else:
            meals = meals.order_by('-'+orderBy)
            mealsNum = meals.count()

        return JsonResponse({"status": 'Success', 'result': get_meal_results(meals[sl]), 'nowOrder': (rangeMeals-1)*6 + 1, 'mealsNum': mealsNum})


def get_meal_results(meals):
    results = []

    for meal in meals:
        results.append(
            {
                "name": meal.name,
                "description": meal.description,
                "imageUrl": meal.imageUrl,
                "countryOfOrigin": meal.countryOfOrigin,
                "user": str(meal.user),
                "dateAdded": meal.dateAdded,
                "id": int(meal.pk),
                "avgRating": int(meal.avgRating()),
                "numberOfVotes": int(meal.numberOfVotes()),
                'comparisonDate': str(meal.comparisonDate())
            }
        )

    return results


def meal_detail_axios(request, pk):
    if request.method == "GET":
        meal = Meal.objects.get(id=pk)
        results = []

        results.append(
            {
                "totalRating": meal.totalRating(),
                "votes": meal.numberOfVotes(),
            }
        )
        return JsonResponse(results, safe=False)

    if request.method == "POST":
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.meal_id = pk
            rating.user = request.user
            rating.save()
            form.save()
            return JsonResponse({"status": 'Success'})
        else:
            return HttpResponseServerError()
