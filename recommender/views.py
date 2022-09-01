from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Meal, Tag
from .forms import CreateForm, DetailForm
from django.http import JsonResponse, HttpResponseServerError
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'index.html'
    model = Meal
    fields = ('name', 'description', 'imageUrl',
              'countryOfOrigin', 'typicalMealTime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["recentlyAdded"] = Meal.objects.all().order_by(
            '-dateAdded')[0:3]

        return context


class MealCreateView(LoginRequiredMixin, FormView):
    template_name = 'recommender/create.html'
    form_class = CreateForm
    success_url = reverse_lazy('recommender:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()

        return context

    def form_valid(self, form):
        print(form)
        print("=========")
        data = form.save(commit=False)
        print("=========")
        print(data)
        data.user = self.request.user
        data.save()
        print(data.user)
        tag_list = self.request.POST.get('tag').split(",")
        print(tag_list)

        if tag_list:
            for tag in tag_list:
                data.tag.add(
                    Tag.objects.get(id=tag))

        form.save_m2m()
        return super().form_valid(form)


class MealDetail(DetailView):
    template_name: str = 'recommender/detail.html'
    model = Meal
    context_object_name = "meal"


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
