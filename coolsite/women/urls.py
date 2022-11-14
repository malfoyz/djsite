from django.urls import (
    path,
    re_path,
)

from .views import *   # отсюда берем функции/классы представления = обработчики маршрутов ниже

urlpatterns = [        # маршруты приложения
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<slug:cat_slug>/', show_category, name="category")
]