from django.http import (
    HttpRequest, 
    HttpResponse, 
    HttpResponseNotFound, 
    Http404,
)
from django.shortcuts import (
    render, 
    redirect,
    get_object_or_404,
)

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'}, 
        {'title': 'Обратная связь', 'url_name': 'contact'}, 
        {'title': 'Войти', 'url_name': 'login'}
]

def index(request: HttpRequest) -> HttpResponse:
    """Обработчик главной страницы"""

    #posts = Women.objects.all()

    context = {
        #'posts': posts,
        'menu': menu, 
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(
        request=request, 
        template_name='women/index.html', 
        context=context,
    )


def about(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы - О сайте"""

    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы добавления статьи"""

    context = {
        'menu': menu,
        'title': 'Добавление статьи'
    }

    return render(
        request=request,
        template_name='women/addpage.html',
        context=context,
    )


def contact(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы обратной связи"""

    return HttpResponse('Обратная связь')


def login(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы авторизации"""

    return HttpResponse('Авторизация')


def pageNotFound(request: HttpRequest, exception):
    """Обработчик для страниц с ошибкой 404"""

    return HttpResponseNotFound('<h1>Страница не найдена</h1>')    # возвращение страницы с кодом 404 (а не 200)


def show_post(request: HttpRequest, post_slug) -> HttpResponse:
    """Обрабтчик страницы поста"""

    post = get_object_or_404(Women, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(
        request=request,
        template_name='women/post.html',
        context=context,
    )


def show_category(request: HttpRequest, cat_id: int) -> HttpResponse:
    """Обработчик страницы категории"""

    #posts = Women.objects.filter(cat_id=cat_id)    # фильтрация постов

    #if len(posts) == 0:
    #    raise Http404()           # перенаправит на функцию pageNotFound

    context = {
        #'posts': posts,
        'menu': menu, 
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }

    return render(
        request=request, 
        template_name='women/index.html', 
        context=context,
    )