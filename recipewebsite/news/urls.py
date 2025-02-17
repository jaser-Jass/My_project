from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register, CustomLoginView

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='news-delete'),
    path('register/', views.register, name='registration_register'),  # регистрация без article_id
    path('register/<int:article_id>/', views.register, name='registration_register_with_article'),  # регистрация с article_id
    path('login/', CustomLoginView.as_view(), name='login'),
]