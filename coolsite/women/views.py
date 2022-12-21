from django.http import (
    HttpRequest, 
    HttpResponse, 
    HttpResponseNotFound, 
)
from django.shortcuts import (
    render, 
    redirect,
    get_object_or_404,
)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)

from .forms import *
from .models import *


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'}, 
        {'title': 'Обратная связь', 'url_name': 'contact'}, 
        {'title': 'Войти', 'url_name': 'login'}
]


class WomenHome(ListView):
    """Класс-обработчик главной страницы"""

    model = Women                                    # выбирает все записи из таблицы в виде списка
    template_name = 'women/index.html'
    context_object_name = 'posts'                    # название, используемое в html-шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Функция генерации существующего контекста + добавления нового контекста.
        Генерирует как динамический, так и статический контекст.
        """

        context = super().get_context_data(**kwargs)              # получение уже существующего контекста ListView
        context['menu'] = menu                                    # создание контекста
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0

        return context

    def get_queryset(self):
        """Функция, фильтрующая объекты"""

        return Women.objects.filter(is_published=True)


# def index(request: HttpRequest) -> HttpResponse:
#     """Обработчик главной страницы"""

#     #posts = Women.objects.all()

#     context = {
#         #'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }

#     return render(
#         request=request,
#         template_name='women/index.html',
#         context=context,
#     )


def about(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы - О сайте"""

    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(CreateView):
    """Класс-обработчик страницы с добавлением поста"""

    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu

        return context




# def addpage(request: HttpRequest) -> HttpResponse:
#     """Обработчик страницы добавления статьи"""

#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()

#     context = {
#         'form': form,
#         'menu': menu,
#         'title': 'Добавление статьи'
#     }

#     return render(
#         request=request,
#         template_name='women/addpage.html',
#         context=context,
#     )


def contact(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы обратной связи"""

    return HttpResponse('Обратная связь')


def login(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы авторизации"""

    return HttpResponse('Авторизация')


def pageNotFound(request: HttpRequest, exception):
    """Обработчик для страниц с ошибкой 404"""

    return HttpResponseNotFound('<h1>Страница не найдена</h1>')    # возвращение страницы с кодом 404 (а не 200)


# def show_post(request: HttpRequest, post_slug) -> HttpResponse:
#     """Обрабтчик страницы поста"""

#     post = get_object_or_404(Women, slug=post_slug)

#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }

#     return render(
#         request=request,
#         template_name='women/post.html',
#         context=context,
#     )

class ShowPost(DetailView):
    """Класс-обработчик отображения определенного поста"""

    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu

        return context



class WomenCategory(ListView):
    """Класс-обработчик отображения страницы определенной категории"""

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False              # страница 404, если записей не будет

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Функция генерации существующего контекста + добавления нового контекста.
        Генерирует как динамический, так и статический контекст.
        """

        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id

        return context



# def show_category(request: HttpRequest, cat_slug) -> HttpResponse:
#     """Обработчик страницы категории"""

#     category = get_object_or_404(Category, slug=cat_slug)

#     context = {
#         #'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': category.id,
#     }

#     return render(
#         request=request,
#         template_name='women/index.html',
#         context=context,
#     )