from django.http import (
    HttpRequest, 
    HttpResponse, 
    HttpResponseNotFound, 
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import auth
from django.contrib.auth import (
    login, 
    logout,
)
from django.core.paginator import Paginator

from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    """Класс представления главной страницы"""

    model = Women                                    # выбирает все записи из таблицы в виде списка
    template_name = 'women/index.html'
    context_object_name = 'posts'                    # название, используемое в html-шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Функция генерации существующего контекста + добавления нового контекста.
        Генерирует как динамический, так и статический контекст.
        """

        context = super().get_context_data(**kwargs)              # получение уже существующего контекста ListView
        c_def = self.get_user_context(title="Главная страница")

        return context | c_def

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

    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """Класс представления страницы с добавлением поста"""

    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context =  super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')

        return context | c_def




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

class ShowPost(DataMixin, DetailView):
    """Класс представления отображения определенного поста"""

    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])

        return context | c_def



class WomenCategory(DataMixin, ListView):
    """Класс представления отображения страницы определенной категории"""

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
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)

        return context | c_def



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


class RegisterUser(DataMixin, CreateView):
    """Класс представления регистрации на сайте"""

    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        
        return context | c_def

    def form_valid(self, form):
        """Вызывается при успешной проверке формы регистрации"""

        user = form.save()            # добавляем пользователя в БД
        auth.login(self.request, user)     # авторизовываем пользователя
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    """Класс представления авторизации на сайте"""

    form_class = AuthenticationForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        
        return context | c_def

    def get_success_url(self):
        """Функция перенаправления на страницу home в случае успешного ввода логина и пароля"""

        return reverse_lazy('home')


def logout_user(request):
    """Обработчик выхода"""

    logout(request)
    return redirect('login')