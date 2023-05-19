from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from .utils import DataMixin
from .forms import *


class ArticlesMain(DataMixin, ListView):
    model = Articles
    paginate_by = 3
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    cats = Category.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('search')

        if query is not None:
            object_list = Articles.objects.filter(
                title__iregex=query, acceptance_stage=1
            ).select_related('user', 'cat').prefetch_related('user__profile')
        else:
            object_list = Articles.objects.filter(acceptance_stage=1)\
                .select_related('user', 'cat')\
                .prefetch_related('user__profile')
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница", cat_selected=0)
        return context | c_def


class CategoryArticles(DataMixin, ListView):
    model = Articles
    paginate_by = 3
    template_name = 'articles/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        query = self.request.GET.get('search')

        if query is not None:
            object_list = Articles.objects.filter(
                cat__slug=self.kwargs['cat_slug'],
                title__iregex=query,
                acceptance_stage=1
            ).select_related('cat', 'user').prefetch_related('user__profile')
        else:
            object_list = Articles.objects.filter(
                cat__slug=self.kwargs['cat_slug'],
                acceptance_stage=1
            ).select_related('cat', 'user').prefetch_related('user__profile')

        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['articles']:
            context['title'] = str(context['articles'][0].cat)
            context['cat_selected'] = context['articles'][0].cat_id
        c_def = self.get_user_context()

        return context | c_def


class AddArticle(DataMixin, CreateView):
    form_class = ArticleForm
    template_name = 'articles/add_article.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить публикацию')

        return context | c_def


class UpdateArticle(UpdateView):
    model = Articles
    form_class = ArticleForm
    template_name = 'articles/update_article.html'
    success_url = reverse_lazy('work')
    extra_context = {"title": "Редактировать статью"}


class Work(TemplateView):
    template_name = "articles/work.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Работа"
        article = Articles.objects.filter(acceptance_stage=0).order_by('time_create').first()
        if article:
            context['article'] = article

        return context


def update_acceptance(request):
    if request.POST:
        article = Articles.objects.filter(acceptance_stage=0).order_by('time_create').first()
        article.acceptance_stage = request.POST['result']
        article.save()
    return redirect('work')


def about(request):
    return render(request, "articles/about.html", {"title": "О нас"})


